
import type { ErrorResponse, CustomError } from '$lib/types/error_model';


export const convertError = (detail: (string | Array<CustomError>)): ErrorResponse => {
  if (typeof detail === 'string') {
    return { error: { msg: detail, type: 'all', input: null, loc: [] } };
  } else {
    const errRes = {} as ErrorResponse;
    for (const error of detail) {
      for (const loc of error.loc) {
        if (errRes[loc] === undefined) errRes[loc] = error;
      }
    }
    return errRes;
  }
} 