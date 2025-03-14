import { TokenService } from "./TokenService";

export class RefreshTokenService extends TokenService {
  public key = "refresh_token";
}

export const refreshTokenService = new RefreshTokenService();
