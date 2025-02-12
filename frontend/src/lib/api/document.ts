import type { DocResponse } from "$lib/types/document";
import { convertErrorFormat } from "$lib/api/default";

export const renderDocument = async (base_url_: string, token: string, document_id: string) => {
    let isSuccess:boolean = false;
    let status:number = 0;
    
    return fetch(`${base_url_}/document/${document_id}/render`, {
        headers: {Authorization: `Bearer ${token}`}
    }).then(res => {
        isSuccess = res.ok; 
        status = res.status;
        return res.json();
    }).then(body => {
        if (isSuccess) {
            return { success: true, status: status, id: body.id, type: 1 } as DocResponse;
        } else {
            const errors = convertErrorFormat(body.details);
            return { success: false, status: status, errors: errors } as DocResponse;
        }
    });
}

export const uploadDocument = async (base_url: string, token: string, data: FormData) => {
    let isSuccess:boolean = false;
    let status:number = 0;

    return fetch(`${base_url}/document/upload`, {
        method: 'POST',
        headers: {Authorization: `Bearer ${token}`},
        body: data
    }).then(res => {
        isSuccess = res.ok;
        status = res.status;
        return res.json();
    }).then(body => {
        if (isSuccess) {
            return { success: true, status: status, id: body.id, type: 1} as DocResponse;
        } else {
            const errors = convertErrorFormat(body.details);
            return { success: false, status: status, errors: errors } as DocResponse;
        }
    })
}

