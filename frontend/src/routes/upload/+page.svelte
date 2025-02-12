<script lang="ts">
    import { FileDropzone } from '@skeletonlabs/skeleton';
    import { get } from 'svelte/store';
    import { local } from '$lib/stores/token';
    import { goto } from '$app/navigation';

    const fileInfo = {
        message: "이곳에 요약할 문서 파일를 업로드 해 주세요",
        meta: "이곳에는 pdf 파일만 업로드 가능합니다",
        isUploaded: false
    }
    let files: FileList;


    const onChangeHandler = (e) => {
        if (e.target.files.length === 0) return;
        fileInfo.message = e.target.files[0].name;
        fileInfo.meta = (e.target.files[0].size / (1024 * 1024)).toFixed(2) + "MB"; 
        fileInfo.isUploaded = true;
    };

    const onSubmitUpload = async () => {
        const formData = new FormData();
        formData.append('file', files[0]);
        const response = await fetch('/upload', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${get(local).token}`,
                'enctype': 'multipart/form-data',
                'Content-Type': 'application/pdf'
            },
            body: formData
        });
        if (response.ok) {
            const body = await response.json();
            goto(`/viewer/${body.id}`);
        } else {
            fileInfo.message = "파일 업로드에 실패했습니다. 다시 시도해 주세요";
        }
    }
</script>

<section class="flex flex-col items-center justify-center px-6 py-8 mx-auto">
<div class="w-full bg-white rounded-lg shadow dark:border sm:max-w-md xl:p-0 dark:bg-surface-800 dark:border-gray-700">
<div class="p-6 space-y-4 md:space-y-6 sm:p-8">

    <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white mx-auto">
        파일 업로드
    </h1>
    <FileDropzone name="files" on:change={onChangeHandler} bind:files={files} accept=".pdf">
        <svelte:fragment slot="lead">
            {#if fileInfo.isUploaded }
                <img src="/pdf_icon.png" alt="pdf icon" class="w-12 h-12 mx-auto">
            {/if}
        </svelte:fragment>
        <svelte:fragment slot="message" >{fileInfo.message}</svelte:fragment>
        <svelte:fragment slot="meta">{fileInfo.meta}</svelte:fragment>
    </FileDropzone>

    <button type="submit" class="btn variant-ghost-primary w-full font-medium rounded-lg text-sm px-5 py-2.5 text-center" on:click preventDefault={onSubmitUpload}>업로드</button>

</div>
</div>
</section>

<style lang="postcss">

</style>