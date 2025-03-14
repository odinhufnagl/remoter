import { call, put } from "redux-saga/effects";
import { authenticateUserFail, authenticateUserSuccess } from "../reducer";

import { UnknownError } from "@/core/errors/defaultErrors";
import { authApi, GetSelfResult } from "@/api";
import { UserEntity } from "@/models/user";

export function* authenticateUserSaga() {
  try {
    const result: GetSelfResult = yield call(authApi.getSelf);
    if (result.isFailure) {
      yield put(
        authenticateUserFail({ error: result.errorValue() as UnknownError })
      );
      return;
    }
    const data: UserEntity = result.getValue().data;
    yield put(authenticateUserSuccess({ user: data }));
  } catch (e) {
    yield put(
      authenticateUserFail({ error: new UnknownError((e as any)?.message) })
    );
  }
}
