import { ResultError } from "../types/ResultError";

export class UnknownError extends ResultError {
  public constructor(message = "Unknown Error") {
    super(0, message, undefined, false);
    this.code = 0;
  }
}
