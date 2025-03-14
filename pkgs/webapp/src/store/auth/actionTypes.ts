import { TokenCredentials } from "@/api/auth/types";
import { ApiError } from "@/api/types";
import { UnknownError } from "@/core/errors/defaultErrors";
import { UserEntity } from "@/models/user";

export enum AuthActionTypes {
  LOGIN_SUCCESS = "LOGIN_SUCCESS",
  LOGIN_FAIL = "LOGIN_FAIL",
}

export type AuthenticateUserSuccessAction = {
  type: string;
  payload: { user: UserEntity };
};

export type AuthenticateUserFailAction = {
  type: string;
  payload: { error: ApiError | UnknownError };
};

export type LoginSuccessAction = {
  type: string;
  payload: { user: UserEntity };
};

export type LoginFailAction = {
  type: string;
  payload: { error: ApiError };
};

export type LogoutAction = {
  type: string;
};

export type LoginAction = {
  type: string;
  payload: { email: string; password: string };
};

export type SetAccessTokenAction = {
  type: string;
  payload: string;
};

export type SetRefreshTokenAction = {
  type: string;
  payload: string;
};

export type saveCredentialsAction = {
  type: string;
  payload: TokenCredentials;
};
