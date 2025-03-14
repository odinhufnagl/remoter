import { SetRefreshTokenAction } from "../actionTypes";
import { refreshTokenService } from "@/services/RefreshTokenService";

export function* setRefreshTokenSaga(action: SetRefreshTokenAction) {
  refreshTokenService.save(action.payload);
}
