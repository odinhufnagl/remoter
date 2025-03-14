import { ResultError } from "@/core/types/ResultError";

export enum STATUS {
  LOADING = "loading",
  SUCCESS = "success",
  ERROR = "error",
  NOT_INITIALIZED = "not_initialized",
  INITIALIZED = "initialized",
}

export type StateResult<Data, Err extends ResultError> = {
  data: Data | null;
  status: STATUS | null;
  err: Err | null;
};

export const resetStateResult = <Date, Err extends ResultError>(
  stateResult: StateResult<Date, Err>
) => {
  stateResult.data = null;
  stateResult.err = null;
  stateResult.status = null;
};
