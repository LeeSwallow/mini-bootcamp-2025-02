<script lang="ts">
    import { FileDropzone } from '@skeletonlabs/skeleton';
    import { getModalStore } from '@skeletonlabs/skeleton';
    import { uploadDocument } from '$lib/api/frontend/upload'
    import { fileUploadErrorModal, fileUploadSuccessModel, noFileErrorModal } from '$lib/components/filezoneModal'

    const modalStore = getModalStore();

    let dropzoneMsg = "( pdf 형식의 문서를 넣어 주세요 )";
    let droppedFiles: FileList | undefined = undefined;
    let targetFile: File | null = null;

    $: if (droppedFiles) {
        console.log(droppedFiles);
        targetFile = droppedFiles[0];
        dropzoneMsg = `( 추가된 파일: ${targetFile.name} )`;
    }

    const onUploadClick = async () => {
        // 파일이 추가되지 않았을 경우
        if (!targetFile) {
            modalStore.trigger(noFileErrorModal);
            return;
        } 
        // 파일 업로드
        const response = await uploadDocument('/upload', targetFile);
        console.log(response);
    }
    const docs: any = []
    for (let i = 0; i < 10; i++) {
        docs.push({
            title: `Document ${i + 1}`,
            thumbnail: "/pdf_icon.png"
        })
    }

</script>

<section class="flex px-6 py-8 w-full">
<div class="w-full bg-white rounded-lg shadow dark:border dark:bg-surface-800 dark:border-gray-700 flex flex-col">
<div class="p-6 sm:p-8">
    
<div id="header">
    <h1 class="text-xxl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white mx-auto my-4">
        사용자 허브
    </h1>
</div>

<hr class="my-4">

<div id="dropzone" class="w-full my-2 py-2 justify-center">
    <h2 class="text-xl font-semibold my-2">문서 추가</h2>
    <div class="text-lg m-4">요약하고 싶은 문서가 있다면 여기에 끌어다 놓으세요</div>
    <FileDropzone name="files" accept="application/pdf" bind:files={droppedFiles}>
        <svelte:fragment slot="message">{dropzoneMsg}</svelte:fragment>
    </FileDropzone>
    <button class="btn variant-ghost-secondary my-6 w-full" on:click={onUploadClick}>업로드 하기</button>
</div>

<hr class="my-4">

<div id="docs" class="my-2 py-2">
    <h2 class="text-xl font-semibold">최근 문서</h2>
    <div class="text-lg m-4">최근에 업로드된 문서 목록입니다.</div>
    <div  class="my-6 flex flex-wrap">
    {#each docs as doc}
        <div class="w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/5 xl:w-1/6">
            <a href="@">
            <div class="bg-gray-100 m-3 p-4 rounded-lg shadow hover:bg-gray-200 dark:bg-surface-600 dark:border dark:hover:bg-surface-400 dark:border-gray-700">
            <img src={doc.thumbnail} alt={doc.title} class="w-full h-auto object-cover mb-2"/>
            <h2 class="text-lg font-semibold">{doc.title}</h2>
            </div>
            </a>
        </div>
    {/each}
    </div>
</div>

</div>
</div>
</section>