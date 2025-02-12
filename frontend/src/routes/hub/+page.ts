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

    const documentsWithThumbnails: Document[] = await Promise.all(
        documents.map(async (doc: Document) => {
            if (doc.thumbnail_path) {
                try {
                    const thumbRes = await fetch(`/api/image/documents/${doc.id}/thumbnail`, {
                        headers: {
                            'Authorization': `Bearer ${curr_token}`
                        }
                    });
                    if (thumbRes.ok) {
                        const blob = await thumbRes.blob();
                        doc.thumbnail_path = URL.createObjectURL(blob);
                    }
                } catch (error) {
                    console.error('Thumbnail load error:', error);
                    doc.thumbnail_path = undefined;
                }
            }
            return doc;
        })
    );
    console.log('Documents:', documentsWithThumbnails);

    return { documents: documentsWithThumbnails };
};