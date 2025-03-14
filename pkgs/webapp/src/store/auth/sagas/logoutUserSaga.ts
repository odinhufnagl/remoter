import { put } from "redux-saga/effects";

import { authActions } from "../reducer";

export function* logoutUserSaga() {
  //yield call([apiClient, apiClient.logout]);
  yield put(authActions.clearCredentials());
}
