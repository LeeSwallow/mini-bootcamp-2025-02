import type { PageLoad } from './$types';
import type { User } from '$lib/types/user_model';
import { token } from '$lib/stores/token';
import { user_id } from '$lib/stores/user';
import { get } from 'svelte/store';
import { goto } from '$app/navigation';

export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {
    try {
        const curr_token:string = get( token ) as string;
        if (!curr_token) { throw new Error('Unauthorized'); }
        const res = await fetch('/api/get/users/self', { method: 'GET', headers: { 'Authorization': `Bearer ${curr_token}` } });
        
        if (!res.ok) { throw new Error('Unauthorized'); }
        const resbody = await res.json() as User;
        
        return { user: resbody };
    } catch (error) {

        console.error('Error:', error);
        goto('/').then(() => {
            token.set(null); user_id.set(null);
        })
    }
}