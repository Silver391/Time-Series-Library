
model_name=TimesNet
python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path /root/autodl-tmp/ \
  --data_path 20240226_tmp.csv \
  --model_id custom_timesnet \
  --model $model_name \
  --data custom \
  --freq s \
  --features MS \
  --target 93 \
  --seq_len 256 \
  --label_len 128 \
  --pred_len 1 \
  --e_layers 2 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 93 \
  --dec_in 93 \
  --c_out 1 \
  --des 'Exp' \
  --d_model 32 \
  --d_ff 32 \
  --top_k 5 \
  --itr 1