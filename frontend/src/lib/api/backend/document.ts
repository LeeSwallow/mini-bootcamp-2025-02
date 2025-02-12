import type { DocResponse } from "$lib/types/document";
import { convertErrorFormat } from "$lib/api/backend/default";

export const renderDocument = async (base_url_: string, token: string, document_id: string) => {
    let isSuccess:boolean = false;
    let status:number = 0;
    const url = `${base_url_}/documents/${document_id}/render`;
    console.log(url);
    return fetch(url, {
        headers: {Authorization: `Bearer ${token}`}
    }).then(res => {
        isSuccess = res.ok; 
        status = res.status;
        return res.json();
    }).then(body => {
        console.log(body);
        if (isSuccess) {
            return { success: true, status: status, id: body.id, type: 1 } as DocResponse;
        } else {
            const errors = convertErrorFormat(body.details);
            return { success: false, status: status, errors: errors } as DocResponse;
        }
    }).catch(err => {
        return { success: false, status: 500, type: 0, errors: { all: '서버에 내부적인 문제가 발생했습니다.' } } as DocResponse;
    })
}

export const uploadDocument = async (base_url: string, token: string, data: FormData) => {
    let isSuccess:boolean = false;
    let status:number = 0;
    const url = `${base_url}/documents/upload`;
    console.log(url);
    
    return fetch(url, {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${token}`,
            ContentType: 'multipart/form-data'
        },
        body: data
    }).then(res => {
        isSuccess = res.ok;
        status = res.status;
        return res.json();
    }).then(body => {
        console.log(body);
        if (isSuccess) {
            return { success: true, status: status, id: body.id, type: 1} as DocResponse;
        } else {
            const errors = convertErrorFormat(body.details);
            return { success: false, status: status, errors: errors } as DocResponse;
        }
    }).catch(err => {
        return { success: false, status: 500, type: 0, errors: { all: '서버에 내부적인 문제가 발생했습니다.' } } as DocResponse;
    })
}

