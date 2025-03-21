import ApiClient, { apiClient } from "../ApiClient";
import { ApiResult } from "../types";
import {
  ApiKeyResponseBody,
  LoginApiPayload,
  SignupApiPayload,
  TokenCredentials,
  TokenCredentialsResponseBody,
} from "./types";
import { tokenCredentialsParser } from "./parsers";
import { UserEntity } from "@/models/user";

export type GetSelfResult = ApiResult<UserEntity>;
export type LoginResult = ApiResult<TokenCredentials>;
export type SignupResult = ApiResult<TokenCredentials>;
export type LogoutResult = ApiResult<void>;

export class AuthApi {
  constructor(private readonly client: ApiClient) {}

  getSelf = async (): Promise<GetSelfResult> =>
    await this.client.fetch({ method: "GET", path: "/v1/auth/self" });

  login = async (data: LoginApiPayload): Promise<LoginResult> => {
    const res = await this.client.fetch<
      TokenCredentialsResponseBody,
      TokenCredentials
    >({
      method: "POST",
      path: "/v1/auth/login",
      body: JSON.stringify(data),
      successParser: tokenCredentialsParser,
    });
    return res;
  };

  signup = async (data: SignupApiPayload): Promise<SignupResult> => {
    const res = await this.client.fetch<
      TokenCredentialsResponseBody,
      TokenCredentials
    >({
      method: "POST",
      path: "/v1/auth/signup",
      body: JSON.stringify(data),
      successParser: tokenCredentialsParser,
    });
    return res;
  };

  logout = async (): Promise<LogoutResult> => {
    const res = await this.client.fetch<void, void>({
      method: "POST",
      path: "/v1/auth/logout",
    });

    return res;
  };

  createApiKey = async (): Promise<ApiResult<string>> =>
    await this.client.fetch<ApiKeyResponseBody, string>({
      method: "POST",
      path: "/v1/auth/api-key",
      successParser: (data: ApiKeyResponseBody) => data.api_key,
    });
}

export const authApi = new AuthApi(apiClient);
