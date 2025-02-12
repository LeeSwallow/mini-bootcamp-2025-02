<script lang="ts">
    import { getModalStore } from '@skeletonlabs/skeleton';
    import { ConfirmSignUpModal } from '$lib/components/modal';
    import { token } from '$lib/stores/token.js';
    import { user_id } from '$lib/stores/user.js';
    import { convertError } from '$lib/service/errors';
    
    const modalStore = getModalStore();

    const field = {email: '', login_id: '', username: '', password1: '', password2: ''};
    const fieldError : Record<string, string> = {all: '',email: '',login_id: '',username: '',password1: '',password2: ''};
    $: serverErrorCheck = fieldError.all.length > 0;
    $: emailErrorCheck = fieldError.email.length > 0;
    $: userIdErrorCheck = fieldError.login_id.length > 0;
    $: usernameErrorCheck = fieldError.username.length > 0;
    $: password1ErrorCheck = fieldError.password1.length > 0;
    $: password2ErrorCheck = fieldError.password2.length > 0;

    const handleSubmit = async (event: Event) => {
        const res = await fetch('/api/post/json/auth/signup', {
            method: 'POST',
            body: JSON.stringify(field)
        });
        const body = await res.json();
        if (res.ok) {
            token.set(body.access_token);
            user_id.set(body.sub);
            modalStore.trigger(ConfirmSignUpModal);
        } else {
            const error = convertError(body.detail);
            for (const key of Object.keys(fieldError)) {
                fieldError[key] = (error[key]) ? error[key].msg : '';
            }
        }
    }
</script>

<section class="flex flex-col items-center justify-center px-6 py-8 mx-auto">
<div class="w-full bg-white rounded-lg shadow dark:border sm:max-w-md xl:p-0 dark:bg-surface-800 dark:border-gray-700">
<div class="p-6 space-y-4 md:space-y-6 sm:p-8">

<h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
    회원가입
</h1>
<form class="space-y-4 md:space-y-6" method="post" on:submit|preventDefault={handleSubmit}>
    
    {#if serverErrorCheck}
        <div class="text-red-500 dark:text-red-400">
            {fieldError.all}
        </div>
    {/if}

    <div>
        <label for="email" class="label block mb-2 text-sm font-medium">Your email</label>
        <input type="email" name="email" id="email" class="input block w-full p-2.5" placeholder="name@company.com" required>
    </div>

    {#if emailErrorCheck && !serverErrorCheck}
        <div class="text-red-500 dark:text-red-400">
            {fieldError.email}
        </div>
    {/if}

    <div>
        <label for="login_id" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">사용자 ID</label>
        <input type="input" name="login_id" id="login_id" class="input block w-full p-2.5" required>
    </div>

    {#if userIdErrorCheck && !serverErrorCheck}
        <div class="text-red-500 dark:text-red-400">
            {fieldError.login_id}
        </div>
    {/if}

    <div>
        <label for="username" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">사용자 이름</label>
        <input type="input" name="username" id="username" class="input block w-full p-2.5" required>
    </div>
    {#if usernameErrorCheck && !serverErrorCheck}
        <div class="text-red-500 dark:text-red-400">
            {fieldError.username}
        </div>
    {/if}

    <div>
        <label for="password1" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">비밀번호</label>
        <input type="password" name="password1" id="password1" placeholder="••••••••" class="input block w-full p-2.5" required>
    </div>

    {#if password1ErrorCheck && !serverErrorCheck}
        <div class="text-red-500 dark:text-red-400">
            {fieldError.password1}
        </div>
    {/if}

    <div>
        <label for="password2" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">비밀번호 재입력</label>
        <input type="password" name="password2" id="password2" placeholder="••••••••" class="input block w-full p-2.5" required>

    </div>

    {#if password2ErrorCheck && !serverErrorCheck}
        <div class="text-red-500 dark:text-red-400">
            {fieldError.password2}
        </div>
    {/if}
    
    <div class="space-y-4 md:space-y-6">
    </div>
    <button type="submit" class="btn variant-ghost-primary w-full font-medium rounded-lg text-sm px-5 py-2.5 text-center">회원가입</button>
</form>

</div>
</div>
</section>

<style>

</style>