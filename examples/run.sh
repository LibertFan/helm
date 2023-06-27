CUDA_VISIBLE_DEVICES=0 helm-run \
    --conf-paths commands/run_baichuan7b_lsat_specs.conf \
    --suite mmlu \
    --max-eval-instances 10000 \
    --enable-huggingface-models baichuan-inc/baichuan-7B \
    -n 1 

CUDA_VISIBLE_DEVICES=0 helm-run \
    --conf-paths commands/run_bloom7b1_lsat_specs.conf \
    --suite mmlu --max-eval-instances 10000 \
    --enable-huggingface-models bigscience/bloom-7b1  \
    -n 1 

CUDA_VISIBLE_DEVICES=0 helm-run \
    --conf-paths commands/run_bloomz7b1_lsat_specs.conf \
    --suite mmlu --max-eval-instances 10000 \
    --enable-huggingface-models bigscience/bloomz-7b1  \
    -n 1 
    
CUDA_VISIBLE_DEVICES=0 helm-run \
    --conf-paths commands/run_bloomzv1_lsat_specs.conf \
    --suite mmlu --max-eval-instances 10000 \
    --enable-huggingface-models disc_llms/bloomz-v1 \
    -n 1 
    
CUDA_VISIBLE_DEVICES=0 helm-run \
    --conf-paths commands/run_bloomzv2_lsat_specs.conf \
    --suite mmlu --max-eval-instances 10000 \
    --enable-huggingface-models disc_llms/bloomz-v2 \
    -n 1 

CUDA_VISIBLE_DEVICES=0 helm-run \
    --conf-paths commands/run_bloom7b1_sogou_lsat_specs.conf \
    --suite mmlu --max-eval-instances 10000 \
    --enable-huggingface-models disc_llms/bloom7b1-sougou \
    -n 1