import { TokenCredentials, TokenCredentialsResponseBody } from "./types";

export const tokenCredentialsParser = (
  data: TokenCredentialsResponseBody
): TokenCredentials => ({
  accessToken: data.access_token,
  refreshToken: data.refresh_token,
});
