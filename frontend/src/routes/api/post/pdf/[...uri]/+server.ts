import type { RequestHandler } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';

// body에 file을 포함하는 multipart/form-data로 POST 요청을 보내는 endpoint 
export const POST: RequestHandler = async ({ params, request }) => {
    const url = `${BACKEND_URL}/${params.uri}`;
    const formData = await request.formData();
    const headers = new Headers();
    headers.set('Authorization', request.headers.get('Authorization') || '');
    const req: RequestInit = { method: 'POST', headers, body: formData};

    return fetch(url, req);
};