import { accessTokenService } from "@/services/AccessTokenService";
import { SetAccessTokenAction } from "../actionTypes";

export function* setAccessTokenSaga(action: SetAccessTokenAction) {
  accessTokenService.save(action.payload);
}
