import type { RequestHandler } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';

export const POST: RequestHandler = async ({ params, request }) => {
    const url = `${BACKEND_URL}/${params.uri}`;
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('Authorization') || ''
    }
    const body = await request.json();
    const req: RequestInit = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
    };
    return await fetch(url, req);
};