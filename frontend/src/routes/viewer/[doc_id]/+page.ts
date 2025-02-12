import type { PageLoad } from './$types';
import type { Document } from '$lib/types/document_model';
import { goto } from '$app/navigation';

export const ssr = false;

export const load: PageLoad = async ({ fetch, params }) => {
    const doc_id = params.doc_id;
    const curr_token = localStorage.getItem('access-token');
    const user_id = localStorage.getItem('user');
    
    if (!curr_token || !user_id) { goto('/login'); return; }

    const document: Document = await fetch(`/api/get/documents/${doc_id}/render`, {
        headers: { 'Authorization': `Bearer ${curr_token}` }
    }).then(res => {
        if (res.ok) {
            console.log('Document Rendered:', res);
            return res.json();
        }
    });
    // props 객체 제거하고 직접 반환
    return { document: document, userId: user_id };
};