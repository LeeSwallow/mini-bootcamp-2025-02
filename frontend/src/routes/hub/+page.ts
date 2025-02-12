import type { PageLoad } from './$types';
import type { Document } from '$lib/types/document_model';
export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {
    const curr_token = localStorage.getItem('access-token');
    if (!curr_token) {
        throw new Error('Unauthorized');
    }
    const resbody = await fetch('/api/get/documents', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${curr_token}`
        }
    }).then(res => res.json());
    const documents = resbody as Array<Document>;
    return { documents };
};