import {
  afterEach,
  describe,
  jest,
  beforeEach,
  it,
  expect,
} from "@jest/globals";
import ApiClient, { axiosInstance } from "./ApiClient";
import { authService } from "@/services/AuthService";
import { Config } from "@/config";
import { ApiError } from "./types";
import { LocalStorageMock } from "@/core/tests/LocalStorageMock";

global.localStorage = new LocalStorageMock();

jest.mock("../config", () => ({
  Config: { apiUrl: "http://localhost:3000" },
}));

describe("ApiClient", () => {
  const expectCallingRefreshToken = async (
    mockRequest: jest.SpiedFunction<typeof axiosInstance.request>
  ) => {
    mockRequest.mockResolvedValue({
      data: {
        accessToken: "new-access-token",
        refreshToken: "new-refresh-token",
      },
    });
    expect(mockRequest).toHaveBeenCalledWith(
      expect.objectContaining({
        method: "POST",
        url: `${Config.apiUrl}${"/v1/auth/refresh"}`,
      })
    );
    expect(mockSaveCredentials).toHaveBeenCalledWith({
      accessToken: "new-access-token",
      refreshToken: "new-refresh-token",
    });
  };

  let mockRequest: jest.SpiedFunction<typeof axiosInstance.request>;
  let mockRefreshToken: jest.SpiedFunction<typeof authService.refreshToken>;
  let mockAccessToken: jest.SpiedFunction<typeof authService.accessToken>;
  let mockSaveCredentials: jest.SpiedFunction<
    typeof authService.saveCredentials
  >;
  const apiClient = new ApiClient(axiosInstance, authService);
  const defaultAccessToken = "accessTokenDefault";
  const defaultRefreshToken = "refreshTokenDefault";
  const defaultErrorBody = {
    error: { message: "error", error_code: 5000 },
  };

  beforeEach(() => {
    mockRequest = jest.spyOn(axiosInstance, "request");
    mockRefreshToken = jest.spyOn(authService, "refreshToken");
    mockAccessToken = jest.spyOn(authService, "accessToken");
    mockSaveCredentials = jest.spyOn(authService, "saveCredentials");
    mockRefreshToken.mockReturnValue(defaultRefreshToken);
    mockAccessToken.mockReturnValue(defaultAccessToken);
    mockSaveCredentials.mockReturnValue(undefined);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe("fetch", () => {
    it("should call request with correct headers", async () => {
      mockRequest.mockResolvedValue({ data: "data" });
      const headers = { "X-Custom-Header": "custom" };
      await apiClient.fetch({ method: "GET", path: "/random-path", headers });
      expect(mockRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          headers: expect.objectContaining({
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: `Bearer ${defaultAccessToken}`,
            ...headers,
          }),
        })
      );
    });
    it("should fetch to correct url with correct method", async () => {
      mockRequest.mockResolvedValue({ data: "data" });
      const method = "POST";
      const path = "/random-path";
      await apiClient.fetch({ method, path });
      expect(mockRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          method,
          url: `${Config.apiUrl}${path}`,
        })
      );
    });
  });
  describe("response", () => {
    it("should return apiresult for success response", async () => {
      mockRequest.mockResolvedValue({ data: { data: [], meta: {} } });
      const result = await apiClient.fetch({ method: "GET", path: "/path" });
      expect(result.isSuccess).toEqual(true);
      expect(result.getValue()).toEqual({ data: { data: [], meta: {} } });
    });
  });
  describe("error", () => {
    it("should logout if error is 401", async () => {
      mockRequest.mockRejectedValue({
        response: { status: 401, data: defaultErrorBody },
        status: 401,
      });
      await apiClient.fetch({ method: "GET", path: "/path" });
    });
    it("should not return authenticationerror if other than 401", async () => {
      mockRequest.mockRejectedValue({
        response: { status: 500, data: defaultErrorBody },
        status: 500,
      });
      const res = await apiClient.fetch({ method: "GET", path: "/path" });
      expect(res.errorValue()?.isUnauthorized()).toEqual(false);
    });
  });
  describe("authentication", () => {
    it("should logout if both refreshtoken and accesstoken is not present and we are not on a authroute", async () => {
      mockAccessToken.mockReturnValue(null);
      mockRefreshToken.mockReturnValue(null);
      mockRequest.mockRejectedValueOnce({
        response: { status: 500, data: defaultErrorBody },
        status: 401,
      });
      const res = await apiClient.fetch({ method: "GET", path: "/path" });
      expect(res.errorValue()?.isUnauthorized()).toEqual(true);
    });
    it("should logout if accesstoken is wrong and refreshtoken is wrong and we are not on a authroute", async () => {
      mockAccessToken.mockReturnValue(defaultAccessToken);
      mockRefreshToken.mockReturnValue(defaultRefreshToken);
      mockRequest.mockRejectedValueOnce({
        response: { status: 500, data: defaultErrorBody },
        status: 401,
      });
      const res = await apiClient.fetch({ method: "GET", path: "/path" });
      expect(res.errorValue()?.isUnauthorized()).toEqual(true);
    });

    it("should not logout if refreshtoken is not present but we are on an authroute", async () => {
      mockRefreshToken.mockReturnValue(null);
      mockRequest.mockRejectedValue({
        response: { status: 500, data: defaultErrorBody },
        status: 500,
      });
      const res = await apiClient.fetch({ method: "GET", path: "/auth/login" });
      expect(res.errorValue()?.isUnauthorized()).toEqual(false);
    });

    it("should try to fetch refreshtoken if there is no accesstoken available ", async () => {
      mockAccessToken.mockReturnValue(null);
      mockRequest.mockResolvedValue({
        data: {
          access_token: "new-access-token",
          refresh_token: defaultRefreshToken,
        },
      });
      await apiClient.fetch({ method: "GET", path: "/path" });

      expect(mockRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          method: "POST",
          url: `${Config.apiUrl}${"/v1/auth/refresh"}`,
        })
      );

      expect(mockSaveCredentials).toHaveBeenCalledWith({
        accessToken: "new-access-token",
        refreshToken: defaultRefreshToken,
      });
    });

    it("should return an unknwown error if there is a fail when fetching the refreshtoken (when accessToken is null)", async () => {
      mockAccessToken.mockReturnValue(null);
      mockRequest.mockRejectedValue({
        response: { status: 500, data: defaultErrorBody },
        status: 500,
      });
      const result = await apiClient.fetch({ method: "GET", path: "/path" });

      expect(mockRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          method: "POST",
          url: `${Config.apiUrl}${"/v1/auth/refresh"}`,
        })
      );
      expect(mockSaveCredentials).not.toHaveBeenCalled();

      expect(result.isFailure).toEqual(true);
      expect(result.errorValue()).toEqual(
        new ApiError(5000, "error", 500, undefined)
      );
    });
    it("should logout if there is a authentication error when fetching the refreshtoken (when accessToken is null)", async () => {
      mockAccessToken.mockReturnValue(null);
      mockRequest.mockRejectedValue({
        response: { status: 401, data: defaultErrorBody },
        status: 401,
      });
      const result = await apiClient.fetch({ method: "GET", path: "/path" });

      expect(mockRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          method: "POST",
          url: `${Config.apiUrl}${"/v1/auth/refresh"}`,
        })
      );
      expect(mockSaveCredentials).not.toHaveBeenCalled();

      expect(result.isFailure).toEqual(true);
      expect(result.errorValue()).toEqual(
        new ApiError(5000, "error", 401, undefined)
      );
    });
    it("should retry request if it was not authenticated (we want to see if the accessToken might have become old)", async () => {
      mockRequest.mockRejectedValueOnce({
        response: { status: 401, data: defaultErrorBody },
        status: 401,
      });
      mockRequest.mockResolvedValueOnce({
        data: {
          accessToken: "new-access-token",
          refreshToken: defaultRefreshToken,
        },
      });
      mockRequest.mockResolvedValueOnce({
        data: "data",
      });
      await apiClient.fetch({ method: "GET", path: "/path" });
      expect(mockRequest).toHaveBeenNthCalledWith(
        1,
        expect.objectContaining({
          method: "GET",
          url: `${Config.apiUrl}/path`,
        })
      );

      expect(mockRequest).toHaveBeenNthCalledWith(
        2,
        expect.objectContaining({
          method: "POST",
          url: `${Config.apiUrl}/v1/auth/refresh`,
        })
      );
      expect(mockSaveCredentials).toHaveBeenCalled();

      expect(mockRequest).toHaveBeenNthCalledWith(
        3,
        expect.objectContaining({
          method: "GET",
          url: `${Config.apiUrl}/path`,
          headers: expect.objectContaining({
            Authorization: `Bearer ${defaultAccessToken}`,
          }),
        })
      );
    });
    it("should logout if we get unauthenticated and retry and get unauthenticated again (meaning the refreshtoken is bad)", async () => {
      mockRequest.mockRejectedValueOnce({
        response: { status: 401, data: defaultErrorBody },
        status: 401,
      });
      mockRequest.mockRejectedValueOnce({
        response: { status: 401, data: defaultErrorBody },
        status: 401,
      });

      const res = await apiClient.fetch({ method: "GET", path: "/path" });
      expect(mockRequest).toHaveBeenNthCalledWith(
        1,
        expect.objectContaining({
          method: "GET",
          url: `${Config.apiUrl}/path`,
        })
      );

      expect(mockRequest).toHaveBeenNthCalledWith(
        2,
        expect.objectContaining({
          method: "POST",
          url: `${Config.apiUrl}/v1/auth/refresh`,
        })
      );
      expect(res.errorValue()?.isUnauthorized()).toEqual(true);
      expect(mockSaveCredentials).not.toHaveBeenCalled();
    });
    it("should not logout if we just get a bad response", async () => {
      mockRequest.mockRejectedValueOnce({
        response: { status: 500, data: defaultErrorBody },
        status: 500,
      });

      await apiClient.fetch({ method: "GET", path: "/path" });
      expect(mockRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          method: "GET",
          url: `${Config.apiUrl}/path`,
        })
      );

      expect(mockSaveCredentials).not.toHaveBeenCalled();
    });
    it("should not logout if we just get a bad response", async () => {
      mockRequest.mockRejectedValueOnce({
        response: { status: 500, data: defaultErrorBody },
        status: 500,
      });

      await apiClient.fetch({ method: "GET", path: "/path" });
      expect(mockRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          method: "GET",
          url: `${Config.apiUrl}/path`,
        })
      );

      expect(mockSaveCredentials).not.toHaveBeenCalled();
    });

    it("should not retry on authRoute ", async () => {
      mockRequest.mockRejectedValueOnce({
        response: { status: 401, data: defaultErrorBody },
        status: 401,
      });
      mockRequest.mockRejectedValueOnce({
        response: { status: 401, data: defaultErrorBody },
        status: 401,
      });

      await apiClient.fetch({ method: "GET", path: "/auth/login" });
      expect(mockRequest).toHaveBeenNthCalledWith(
        1,
        expect.objectContaining({
          method: "GET",
          url: `${Config.apiUrl}/auth/login`,
        })
      );

      expect(mockRequest).not.toHaveBeenNthCalledWith(
        2,
        expect.objectContaining({
          method: "POST",
          url: `${Config.apiUrl}/v1/auth/refresh`,
        })
      );
      expect(mockSaveCredentials).not.toHaveBeenCalled();
    });
  });
});
