import type { RequestHandler } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';

export const GET: RequestHandler = async ({ params, url, request }) => {
    const apiUrl = `${BACKEND_URL}/${params.uri}${url.search}`;
    console.log('GET:', apiUrl);
    const headers = { 'Authorization': request.headers.get('Authorization') || '' }
    const req: RequestInit = {
        method: 'GET',
        headers: headers,
    };
    return await fetch(apiUrl, req);
};