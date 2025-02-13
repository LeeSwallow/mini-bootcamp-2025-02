import type { RequestHandler } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';

export const PUT: RequestHandler = async ({ params, url, request }) => {
    const apiUrl = `${BACKEND_URL}/${params.uri}${url.search}`;
    console.log("PUT",apiUrl);
  
    const body = await request.json();
    const req: RequestInit = {
        method: 'PUT',
        headers: request.headers,
        body: JSON.stringify(body)
    };
    return await fetch(apiUrl, req);
};