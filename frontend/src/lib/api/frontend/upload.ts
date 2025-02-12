import { getToken } from '$lib/stores/token';
import type { DocResponse } from '$lib/types/document';

export const uploadDocument = async (url: string, file: File) => {
    const formData = new FormData();
    const token = getToken().token;
    formData.append('file', file);
    return fetch(url, {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${token}`
        },
        body: formData
    });
};

export const readResponse = async (res: Response) : Promise<DocResponse> => {
    return await res.json();
}
