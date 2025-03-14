import { authApi } from "@/api";
import { ApiError } from "@/api/types";
import { UnknownError } from "@/core/errors/defaultErrors";
import { ResultError } from "@/core/types/ResultError";
import { UserEntity } from "@/models/user";
import { authService } from "@/services/AuthService";
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

const AuthContext = createContext<{
  currentUser: AuthStateResult<UserEntity, ApiError | UnknownError>;
  logout: () => Promise<void>;
} | null>(null);

export enum AUTH_STATUS {
  IDLE = "IDLE",
  LOADING = "LOADING",
  AUTHENTICATED = "AUTHENTICATED",
  NOT_AUTHENTICATED = "NOT_AUTHENTICATED",
  ERROR = "ERROR",
}

export type AuthStateResult<Data, Err extends ResultError> = {
  data: Data | null;
  status: AUTH_STATUS | null;
  err: Err | null;
};

const initialState: AuthStateResult<UserEntity, ApiError | UnknownError> = {
  data: null,
  status: AUTH_STATUS.IDLE,
  err: null,
};

import { ReactNode } from "react";

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [state, setState] = useState(initialState);

  const logout = useCallback(async () => {
    await authService.logout();
    setState({ data: null, status: AUTH_STATUS.NOT_AUTHENTICATED, err: null });
  }, []);

  const authenticateUser = useCallback(async () => {
    setState({
      data: null,
      status: AUTH_STATUS.LOADING,
      err: null,
    });
    const selfResult = await authApi.getSelf();
    if (selfResult.isFailure) {
      if (selfResult.errorValue()?.isUnauthorized()) {
        await logout();
        return;
      }
      setState({
        data: null,
        status: AUTH_STATUS.ERROR,
        err: selfResult.errorValue(),
      });
      return;
    }
    const user = selfResult.getValue().data;
    setState({
      data: user,
      status: AUTH_STATUS.AUTHENTICATED,
      err: null,
    });
  }, [logout]);

  useEffect(() => {
    authenticateUser();
  }, [authenticateUser]);

  return (
    <AuthContext.Provider value={{ currentUser: state, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
