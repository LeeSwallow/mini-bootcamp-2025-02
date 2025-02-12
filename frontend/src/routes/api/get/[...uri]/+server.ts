import type { RequestHandler } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';

export const GET: RequestHandler = async ({ params, request }) => {
    const url = `${BACKEND_URL}/${params.uri}`;
    const headers = { 'Authorization': request.headers.get('Authorization') || '' }
    const req: RequestInit = {
        method: 'GET',
        headers: headers,
    };
    return await fetch(url, req);
};