import type { RequestHandler } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';

export const DELETE: RequestHandler = async ({ params, url, request }) => {
  const apiUrl = `${BACKEND_URL}/${params.uri}${url.search}`;
  console.log("DELETE:", apiUrl);
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': request.headers.get('Authorization') || ''
  }
  const req: RequestInit = {
    method: 'DELETE',
    headers: headers,
  };
  return await fetch(apiUrl, req);
};