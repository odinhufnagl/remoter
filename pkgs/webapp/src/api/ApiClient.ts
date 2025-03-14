import axios, {
  AxiosError,
  AxiosHeaders,
  AxiosInstance,
  AxiosResponse,
  Method,
  ResponseType,
} from "axios";
import { objectToQueryParams, ToQueryParams } from "./utils";
import { ApiError, ApiSuccess } from "./types";
import { Result } from "@/core/types/Result";
import { UnknownError } from "@/core/errors/defaultErrors";
import { TokenCredentials, TokenCredentialsResponseBody } from "./auth/types";
import { Config } from "@/config";
import { tokenCredentialsParser } from "./auth/parsers";
import { authService, AuthService } from "@/services/AuthService";

export const axiosInstance = axios.create({
  baseURL: Config.apiUrl,
});

export default class ApiClient {
  public interceptors = this.client.interceptors;

  constructor(
    private readonly client: AxiosInstance,
    private readonly authService: AuthService
  ) {}

  public async refreshAccessToken(
    refreshToken: string
  ): Promise<TokenCredentials> {
    const method = "POST";
    const path = `/v1/auth/refresh`;
    const body = JSON.stringify({
      refresh_token: refreshToken,
    });
    const response = await this.client.request<TokenCredentialsResponseBody>({
      method,
      url: this.url(path),
      headers: this.mergedHeaders() as AxiosHeaders,
      data: body,
    });

    return tokenCredentialsParser(response.data);
  }

  public async refresh(): Promise<boolean> {
    const refreshToken = this.authService.refreshToken();
    const credentials = await this.refreshAccessToken(refreshToken || "");
    this.authService.saveCredentials(credentials);
    return true;
  }

  private mergedHeaders(
    accessToken?: string,
    headers?: Record<string, unknown>
  ): Record<string, unknown> {
    return Object.assign(
      {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      headers
    );
  }

  private url(path: string, params?: ToQueryParams): string {
    return Config.apiUrl + path + objectToQueryParams(params);
  }

  public isAuthRoute(path: string): boolean {
    return /(\/auth\/login|\/auth\/signup|\/password\/reset-token|\/password\/reset|\auth\/sso\/saml)/.test(
      path
    );
  }

  public async fetch<AR, R>({
    method,
    path,
    body,
    successParser = (data) => data as unknown as R,
    headers = {},
    params,
    isRetryAttempt,
    responseType,
    credentials,
  }: {
    method: Method;
    path: string;
    successParser?: (arg: AR, headers: Record<string, string>) => R;
    body?: string;
    headers?: Record<string, unknown>;
    params?: ToQueryParams;
    isRetryAttempt?: boolean;
    responseType?: ResponseType;
    credentials?: boolean;
  }): Promise<Result<ApiSuccess<R>, ApiError | UnknownError>> {
    const isAuthRoute = this.isAuthRoute(path);

    const accessToken = this.authService.accessToken();
    //const refreshToken = this.storeRegistry.store.getState().auth.refreshToken;
    //const accessToken = this.storeRegistry.store.getState().auth.accessToken;

    if (!accessToken && !isAuthRoute) {
      try {
        await this.refresh();
      } catch (e) {
        return Result.fail(this.parseError(e as AxiosError, isAuthRoute));
      }
    }
    try {
      const response = await this.client.request({
        method,
        url: this.url(path, params),
        headers: this.mergedHeaders(
          accessToken as string,
          headers
        ) as AxiosHeaders,
        data: body,
        responseType,
        withCredentials: Boolean(credentials),
      });
      const success = this.parseSuccess<AR, R>(response, successParser);

      return Result.ok(success);
    } catch (err) {
      if (isRetryAttempt) {
        return Result.fail(this.parseError(err as AxiosError, isAuthRoute));
      }
      if ((err as AxiosError).status === 401 && !isAuthRoute) {
        try {
          await this.refresh();

          return await this.fetch({
            method,
            path,
            body,
            successParser,
            headers,
            params,
            isRetryAttempt: true,
            credentials,
          });
        } catch (e) {
          return Result.fail(this.parseError(err as AxiosError, isAuthRoute));
        }
      }
      return Result.fail(this.parseError(err as AxiosError, isAuthRoute));
    }
  }

  parseSuccess<A, R>(
    response: AxiosResponse<A>,
    parser: (data: A, headers: Record<string, string>) => R
  ): ApiSuccess<R> {
    return {
      status: response.status,
      data: parser(response.data, response.headers as Record<string, string>),
    };
  }

  parseValidationDetails = (details: any) => {
    return details.map((detail: any) => ({
      msg: detail.msg,
    }));
  };

  parseError = (
    err: AxiosError,
    isAuthRoute: boolean
  ): ApiError | UnknownError => {
    const response = err.response;
    const errorBody: any = response?.data;
    if (!errorBody) {
      return new UnknownError();
    }
    /*if (err.status === 401 && !isAuthRoute) {
      this.storeRegistry.store.dispatch(authActions.logout());
    }*/

    if (err.status === 422 && errorBody?.detail) {
      return new ApiError(
        200,
        "Validation Error",
        err.status as number,
        this.parseValidationDetails(errorBody?.detail)
      );
    }
    if (errorBody?.error) {
      return new ApiError(
        errorBody?.error?.error_code,
        errorBody?.error?.message,
        err.status as number,
        errorBody?.error?.data
      );
    }
    console.log("errorBody", errorBody);
    return new UnknownError();
  };
}

export const apiClient = new ApiClient(axiosInstance, authService);
