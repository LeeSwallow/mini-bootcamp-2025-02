export const convertErrorFormat = (details: Array<{loc: Array<string>, msg: string, type: string}>) => {
    const errors: { [key: string]: string } = {};
    let type = -10;
    for (let error of details) {
        const field = error.loc[error.loc.length - 1];
        errors[field] = error.msg;
        if (Number(error.type) < type) {
            type = Number(error.type);
        }
    }
    return errors;
}
