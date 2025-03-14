import { ApiError } from "@/api/types";

export class ResultError<Props = any> {
  public code?: number;
  public message: string;
  public props?: Props;
  public isApiError: boolean;

  public constructor(
    code: number,
    message: string,
    props?: Props,
    isApiError = true
  ) {
    this.code = code;
    this.message = message;
    this.props = props;
    this.isApiError = isApiError;
  }

  public isValidationError(): boolean {
    return this.code === 200;
  }

  public isUnauthorized(): boolean {
    return this instanceof ApiError && this.statusCode === 401;
  }
}
