<script lang="ts">
    import { goto } from '$app/navigation';
    import { setAuth } from '$lib/stores/auth';
    import { enhance } from '$app/forms';
	import type { ActionResult } from '@sveltejs/kit';
    
    const fieldErrors: { [key: string]: string } = {
        all: '',
        login_id: '',
        password: ''
    }
    $: serverError = (fieldErrors.all) ? true : false;
    $: userIdError = (fieldErrors.login_id) ? true : false;
    $: passwordError = (fieldErrors.password) ? true : false;

    /** @type {import('./$types').ActionData}*/
    export let form;

    const MyEnhance = ( { form } ) => {
        return async ({ result }: { result: ActionResult }) => {
            if (result.type === 'success') {
                const res = result.data.body;
                if (res.success) {
                    setAuth(res.token);
                    goto('/');
                } else {
                    if (res.errors) {
                        for (const [key, value] of Object.entries(fieldErrors)) {
                            if (res.errors[key]) {
                                fieldErrors[key] = res.errors[key];
                            } else {
                                fieldErrors[key] = '';
                            }
                        }
                    }
                }
            } else {
                console.error('Unexpected result type:', result.type);
            }
        }  
    }
</script>

<section class="flex flex-col items-center justify-center px-6 py-8 mx-auto">
<div class="w-full bg-white rounded-lg shadow dark:border sm:max-w-md xl:p-0 dark:bg-surface-800 dark:border-gray-700">
<div class="p-6 space-y-4 md:space-y-6 sm:p-8">

<h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
    로그인
</h1>
<!-- 폼 시작 -->
<form class="space-y-4 md:space-y-6" use:enhance={MyEnhance} method="post">
    {#if serverError}
    <div class="text-red-500 dark:text-red-400">
        {fieldErrors.all}
    </div>
    {/if}

    <div>
        <label for="login_id" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">사용자 ID</label>
        <input type="input" name="login_id" id="login_id" class="input block w-full p-2.5"required>
    </div>
    {#if !serverError && userIdError}
        <div class="text-red-500 dark:text-red-400"> 
            {fieldErrors.login_id}
        </div>
    {/if}
    <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">비밀번호</label>
    <input type="password" name="password" id="password" placeholder="••••••••" class="input block w-full p-2.5" required>
    <div class="space-y-4 md:space-y-6">
    
    {#if !serverError && passwordError}
        <div class="text-red-500 dark:text-red-400">
            {fieldErrors.password}
        </div>
    {/if}

    </div>
    <button type="submit" class="btn btn variant-ghost-primary w-full font-medium rounded-lg text-sm px-5 py-2.5 text-center">로그인</button>
    <p class="text-sm font-light text-surface-500 dark:text-surface-400">
        계정이 존재하지 않나요? <a href="/signup" class="font-medium text-primary-600 hover:underline dark:text-primary-500 px-5">회원가입</a>
    </p>
</form>

</div>
</div>
</section>

<style lang="postcss">

</style>