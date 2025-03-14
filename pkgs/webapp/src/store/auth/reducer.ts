import { createSlice } from "@reduxjs/toolkit";
import {
  AuthenticateUserFailAction,
  AuthenticateUserSuccessAction,
  saveCredentialsAction,
  SetAccessTokenAction,
  SetRefreshTokenAction,
} from "./actionTypes";
import { resetStateResult } from "../types";
import { STATUS, StateResult } from "@/store/types";
import { ApiError } from "@/api/types";
import { UnknownError } from "@/core/errors/defaultErrors";
import { UserEntity } from "@/models/user";
import { accessTokenService } from "@/services/AccessTokenService";
import { refreshTokenService } from "@/services/RefreshTokenService";

export type State = {
  currentUser: StateResult<UserEntity, ApiError | UnknownError>;
  accessToken: string | null;
  refreshToken: string | null;
};

const initialState: State = {
  currentUser: { data: null, status: null, err: null },
  accessToken: accessTokenService.get(),
  refreshToken: refreshTokenService.get(),
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    authenticateUser(state) {
      resetStateResult(state.currentUser);
      state.currentUser.status = STATUS.LOADING;
    },
    authenticateUserSuccess(state, action: AuthenticateUserSuccessAction) {
      state.currentUser.data = action.payload.user;
      state.currentUser.status = STATUS.SUCCESS;
    },
    authenticateUserFail(state, action: AuthenticateUserFailAction) {
      state.currentUser.err = action.payload.error;
      state.currentUser.status = STATUS.ERROR;
    },
    logout(state) {
      Object.assign(state, initialState);
    },
    setAccessToken(state, action: SetAccessTokenAction) {
      state.accessToken = action.payload;
    },
    setRefreshToken(state, action: SetRefreshTokenAction) {
      state.refreshToken = action.payload;
    },
    clearCredentials(state) {
      state.accessToken = null;
      state.refreshToken = null;
    },
    saveCredentials(state, action: saveCredentialsAction) {
      state.accessToken = action.payload.accessToken;
      state.refreshToken = action.payload.refreshToken;
    },
  },
});

export const {
  logout,
  authenticateUser,
  authenticateUserSuccess,
  authenticateUserFail,
  setAccessToken,
  setRefreshToken,
  saveCredentials,
  clearCredentials,

  // logout,
} = authSlice.actions;

export const authActions = authSlice.actions;

export const authReducer = authSlice.reducer;
