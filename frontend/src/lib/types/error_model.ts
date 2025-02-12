
export interface CustomError {
    msg: string;
    type: string;
    input: string | null;
    loc: Array<string>;
}

export type ErrorResponse = Record<string, CustomError>;