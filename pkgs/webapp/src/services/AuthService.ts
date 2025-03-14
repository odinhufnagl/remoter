import {
  LoginApiPayload,
  SignupApiPayload,
  TokenCredentials,
} from "@/api/auth/types";
import { accessTokenService } from "./AccessTokenService";
import { refreshTokenService } from "./RefreshTokenService";
import { authApi, LoginResult, SignupResult } from "@/api";

export type LoginDto = LoginApiPayload;
export type SignupDto = SignupApiPayload;

export class AuthService {
  public refreshToken() {
    return refreshTokenService.get();
  }
  public accessToken() {
    return accessTokenService.get();
  }

  public saveCredentials(tokenCredentials: TokenCredentials) {
    accessTokenService.save(tokenCredentials.accessToken);
    refreshTokenService.save(tokenCredentials.refreshToken);
  }
  public clearCredentials() {
    accessTokenService.remove();
    refreshTokenService.remove();
  }

  public async login(data: SignupDto): Promise<LoginResult> {
    const res = await authApi.login(data);
    if (res.isFailure) return res;
    this.saveCredentials(res.getValue().data);
    return res;
  }

  public async signup(data: SignupDto): Promise<SignupResult> {
    const res = await authApi.signup(data);
    if (res.isFailure) return res;
    this.saveCredentials(res.getValue().data);
    return res;
  }

  public async logout(): Promise<void> {
    await authApi.logout();
    this.clearCredentials();
  }
}

export const authService = new AuthService();
