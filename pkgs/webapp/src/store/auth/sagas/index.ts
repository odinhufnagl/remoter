import { takeLatest } from "redux-saga/effects";
import {
  authenticateUser,
  clearCredentials,
  logout,
  saveCredentials,
  setAccessToken,
  setRefreshToken,
} from "../reducer";
import { authenticateUserSaga } from "./authenticateUserSaga";
import { logoutUserSaga } from "./logoutUserSaga";
import { setAccessTokenSaga } from "./setAccessTokenSaga";
import { setRefreshTokenSaga } from "./setRefreshTokenSaga";
import { saveCredentialsSaga } from "./saveCredentialsSaga";
import { clearCredentialsSaga } from "./clearCredentialsSaga";

export const authSagas = [
  takeLatest(authenticateUser.type, authenticateUserSaga),
  takeLatest(logout.type, logoutUserSaga),
  takeLatest(setAccessToken.type, setAccessTokenSaga),
  takeLatest(setRefreshToken.type, setRefreshTokenSaga),
  takeLatest(saveCredentials.type, saveCredentialsSaga),
  takeLatest(clearCredentials.type, clearCredentialsSaga),
];
