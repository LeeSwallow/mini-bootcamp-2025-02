<script context="module" lang="ts">
    export { load } from './+page';
</script>

<script lang="ts">
    import type { Document } from '$lib/types/document_model';
    import { FileDropzone, type ModalSettings } from '@skeletonlabs/skeleton';
    import { getModalStore } from '@skeletonlabs/skeleton';
    import { token } from '$lib/stores/token';
    import { get } from 'svelte/store';
    import { NoFileErrorModal, FileUploadErrorModal, LoadingModal  } from '$lib/components/modal';
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import { goto } from '$app/navigation';

    export let data: { documents: Document[] };
    $: ({ documents } = data);
    const modalStore = getModalStore();

    let dropzoneMsg = "PDF 문서를 여기에 끌어다 놓으세요";
    let droppedFiles: FileList | undefined = undefined;
    let targetFile: File | null = null;
    let visible = false;
    let isLoading = true;

    onMount(() => {
        visible = true;
        isLoading = false;
        for (const doc of documents) {
            if (doc.title.length > 13)
                doc.title = doc.title.slice(0, 9) + '...pdf';
        }
    });

    $: if (droppedFiles) {
        targetFile = droppedFiles[0];
        dropzoneMsg = `( 추가된 파일: ${targetFile.name} )`;
    }

    const uploadSuccessModal = (docid: string) : ModalSettings => {
            return {
                type:"confirm",
                title:"파일 업로드 성공",
                body:"파일 업로드에 성공했습니다. 뷰어로 이동하시겠습니까?",
                buttonTextConfirm: "확인",
                buttonTextCancel: "돌아가기",
                response: (r) => { if (r) {
                    modalStore.trigger(LoadingModal);
                    goto(`/viewer/${docid}`).then(() => {
                        modalStore.clear();
                    });
                }}
            };
        }


    const onUploadClick = async () => {
        // 파일이 추가되지 않았을 경우
        if (!targetFile) {
            modalStore.trigger(NoFileErrorModal); return;
        } 

        const file = targetFile;
        const formData = new FormData();
        formData.append('file', file);
        // 파일 업로드
        fetch('/api/post/pdf/documents/upload', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${get(token)}` },
            body: formData
        }).then(res => {
            if (res.ok) {
                res.json().then(data => {
                    const modal = uploadSuccessModal(data.id);
                    modalStore.trigger(modal);
                    documents = [data, ...documents];
                })
            } else {
                throw new Error('파일 업로드에 실패했습니다.');
            }
        }).catch(err => {
            console.error(err);
            modalStore.trigger(FileUploadErrorModal);
        });
    }
    function deleteDocument(documentId: string) {
        fetch(`/api/delete/documents/${documentId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${get(token)}` }
        }).then(res => {
            if (res.ok) {
                documents = documents.filter(doc => doc.id !== documentId);
            } else {
                throw new Error('파일 삭제에 실패했습니다.');
            }
        }).catch(err => {
            console.error(err);
        });
    }


    function goToViewer(documentId: string) {
        modalStore.trigger(LoadingModal);
        goto(`/viewer/${documentId}`).then(() => {
            modalStore.clear();
        });
    }
</script>

{#if visible}
<section transition:fade={{duration: 100}} class="flex px-6 py-8 w-full">
<div class="w-full bg-white rounded-lg shadow dark:border dark:bg-surface-800 dark:border-gray-700 flex flex-col">
<div class="p-6 sm:p-8">
    
<div id="header" class="mb-8 flex justify-between">
    <h1 class="text-xxl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
        MY HUB
    </h1>
    <button class="btn variant-ghost-warning" on:click={() => goto('/profile')}>
        회원 정보 수정
    </button>
</div>

<hr class="my-6">

<div id="dropzone" class="w-full my-4 py-2 justify-center">
    <h2 class="text-xl font-semibold mb-4">새 문서 업로드</h2>
    <div class="text-lg mb-6">PDF 문서를 업로드하여 빠르게 요약해보세요</div>
    <FileDropzone name="files" accept="application/pdf" bind:files={droppedFiles}>
        <svelte:fragment slot="message"><br>{dropzoneMsg}<br><br></svelte:fragment>
    </FileDropzone>
    <button class="btn variant-ghost-secondary my-8 w-full" on:click|preventDefault={onUploadClick}>문서 업로드</button>
</div>

<hr class="my-6">

<div id="docs" class="my-4 py-2">
    <h2 class="text-xl font-semibold mb-4">내 문서함</h2>
    <div class="text-lg mb-6">업로드한 문서들을 한눈에 확인하세요</div>
    <div class="my-6 flex flex-wrap">
    {#each documents as doc}
        <div class="relative w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/5 xl:w-1/6">
            <div class="justify-center flex flex-col items-center">
            <button class="btn variant-ghost-surface" on:click={() => deleteDocument(doc.id)}>X</button>
            <button on:click={() => goToViewer(doc.id)} class="bg-gray-100 m-3 p-4 rounded-lg shadow hover:bg-gray-200 dark:bg-surface-600 dark:border dark:hover:bg-surface-400 dark:border-gray-700">
            <img src={doc.thumbnail_path || '/images/pdf_icon.png'} alt={doc.title} class="w-[150px] h-[200px] mb-3"/>
            <h2 class="font-semibold truncate overflow-hidden" title={doc.title}>{doc.title}</h2>
            </button>
        </div>
        </div>
    {/each}
    </div>
</div>

</div>
</div>
</section>
{/if}
