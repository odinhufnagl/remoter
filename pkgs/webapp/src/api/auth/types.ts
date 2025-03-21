export type TokenCredentials = {
  refreshToken: string;
  accessToken: string;
};

export type LoginApiPayload = {
  email: string;
  password: string;
};

export type SignupApiPayload = {
  email: string;
  password: string;
};

export type TokenCredentialsResponseBody = {
  access_token: string;
  refresh_token: string;
};

export type ApiKeyResponseBody = {
  api_key: string;
};
