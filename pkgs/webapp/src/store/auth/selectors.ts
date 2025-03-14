import { createSelector } from "@reduxjs/toolkit";
import { getGlobalState } from "..";
import { STATUS } from "../types";

const getAuthState = createSelector(getGlobalState, (state) => state.auth);

export const getCurrentUserResult = createSelector(
  getAuthState,
  (state) => state.currentUser
);

export const isAuthenticated = createSelector(
  getCurrentUserResult,
  (state) => state.status === STATUS.SUCCESS && state.data?.id
);

export const isSelfLoading = createSelector(
  getCurrentUserResult,
  (state) => state.status === STATUS.LOADING
);

export const isSelfError = createSelector(
  getCurrentUserResult,
  (state) => state.status === STATUS.ERROR
);

export const selfError = createSelector(
  getCurrentUserResult,
  (state) => state.err
);

export const getSelf = createSelector(
  getCurrentUserResult,
  (state) => state.data
);

export const getAccessToken = createSelector(
  getAuthState,
  (state) => state.accessToken
);

export const getRefreshToken = createSelector(
  getAuthState,
  (state) => state.refreshToken
);
