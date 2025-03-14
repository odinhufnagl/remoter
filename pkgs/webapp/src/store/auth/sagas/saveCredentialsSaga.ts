import { saveCredentialsAction } from "../actionTypes";
import { authService } from "@/services/AuthService";

export function* saveCredentialsSaga(action: saveCredentialsAction) {
  authService.saveCredentials(action.payload);
}
