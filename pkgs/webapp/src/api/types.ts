import { UnknownError } from "@/core/errors/defaultErrors";
import { Result } from "@/core/types/Result";
import { ResultError } from "@/core/types/ResultError";

export type ApiSuccess<T> = {
  data: T;
  status: number;
};

export class ApiError<Props = undefined> extends ResultError<Props> {
  public statusCode: number;
  public constructor(
    code: number,
    message: string,
    statusCode: number,
    props?: Props
  ) {
    super(code, message, props, true);
    this.statusCode = statusCode;
  }
}

export type ApiResult<T> = Result<ApiSuccess<T>, ApiError | UnknownError>;
