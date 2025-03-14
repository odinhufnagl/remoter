import { TokenService } from "./TokenService";

export class AccessTokenService extends TokenService {
  public key = "access_token";
}

export const accessTokenService = new AccessTokenService();
