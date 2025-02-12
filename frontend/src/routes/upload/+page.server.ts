import type { Actions } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';
import { uploadDocument, renderDocument } from '$lib/api/document';

export const actions: Actions = {
    // pdf 파일을 받아 백엔드로 전송하고 성공 시 그 음답을 반환한다.
    default: async (event) => {
        const formData = await event.request.formData();
        const file = formData.get('file') as File;
        let token = event.request.headers.get('Authorization');
        token = (token?.startsWith('Bearer ')) ? token.slice(7) : '';

        const uploadRes = await uploadDocument(BACKEND_URL, token, formData)
        if (!uploadRes.success) {
            return {
                status: uploadRes.status,
                body: { success: false, type: uploadRes.type, errors: uploadRes.errors }
            }
        }
        const renderRes = await renderDocument(BACKEND_URL, token, uploadRes.id as string);
        if (!renderRes.success) {
            return {
                status: renderRes.status,
                body: { success: false, type: renderRes.type, errors: renderRes.errors }
            }
        } 
        
        return {
            status: renderRes.status,
            body: { success: true, type: renderRes.type, id: uploadRes.id }
        }
    }
};


    