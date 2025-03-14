import { ResultError } from "./ResultError";

export class Result<T, E extends ResultError | null = null> {
  public isSuccess: boolean;
  public isFailure: boolean;
  public error: E | null;
  private _value: T | null;

  public constructor(isSuccess: boolean, error: E | null, value?: T) {
    if (isSuccess && error) {
      throw new Error(
        "InvalidOperation: A result cannot be successful and contain an error"
      );
    }
    if (!isSuccess && !error) {
      throw new Error(
        "InvalidOperation: A failing result needs to contain an error message"
      );
    }

    this.isSuccess = isSuccess;
    this.isFailure = !isSuccess;
    this.error = error === undefined ? null : error;
    this._value = value === undefined ? null : value;

    Object.freeze(this);
  }

  public getValue(): T {
    if (!this.isSuccess || this._value === null || this._value === undefined) {
      throw new Error(
        "Can't get the value of an error result. Use 'errorValue' instead."
      );
    }

    return this._value;
  }

  public errorValue(): E | null {
    return this.error;
  }

  public static ok<U, E extends ResultError>(value?: U): Result<U, E> {
    return new Result<U, E>(true, null, value);
  }

  public static fail<U, E extends ResultError>(error: E | null): Result<U, E> {
    return new Result<U, E>(false, error);
  }

  public static combine(
    results: Result<any, ResultError>[]
  ): Result<any, ResultError> {
    for (const result of results) {
      if (result.isFailure) return result;
    }
    return Result.ok();
  }
}
