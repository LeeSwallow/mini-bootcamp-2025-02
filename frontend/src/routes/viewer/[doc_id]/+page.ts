import type { PageLoad } from './$types';

export const ssr = false;
export const load: PageLoad = async ({ fetch, params }) => {
    const docId = params.doc_id;
    const curr_token = localStorage.getItem('access-token');
    if (!curr_token) {
        throw new Error('Unauthorized');
    }
    const resbody = await fetch('/api/get/doucumets/{docId}', {)

};