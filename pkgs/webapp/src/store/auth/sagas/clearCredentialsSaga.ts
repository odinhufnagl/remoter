import { authService } from "@/services/AuthService";

export function* clearCredentialsSaga() {
  authService.clearCredentials();
}
