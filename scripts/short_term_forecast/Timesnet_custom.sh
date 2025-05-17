  model_name=iTransformer

  python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path /home/lenovo/yinzhou/dataset \
  --data_path 20250101_20250327.csv \
  --test_data_path 20250328_20250328.csv \
  --model_id custom_iTransformer \
  --model $model_name \
  --data custom \
  --features MS \
  --freq s \
  --patience 7 \
  --train_epochs 20 \
  --target 93 \
  --seq_len 512 \
  --label_len 256 \
  --pred_len 1 \
  --e_layers 3 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 92 \
  --dec_in 92 \
  --c_out 1 \
  --des 'Exp' \
  --d_model 512 \
  --d_ff 512 \
  --batch_size 16 \
  --learning_rate 0.0005 \
  --itr 1

model_name=Crossformer

python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path /home/lenovo/yinzhou/dataset \
  --data_path 20250101_20250327.csv \
  --test_data_path 20250328_20250328.csv \
  --model_id custom_crossformer \
  --model $model_name \
  --data custom \
  --features MS \
  --freq s \
  --patience 7 \
  --train_epochs 20 \
  --target 93 \
  --seq_len 512 \
  --label_len 256 \
  --pred_len 1 \
  --e_layers 2 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 92 \
  --dec_in 92 \
  --c_out 1 \
  --d_model 256 \
  --d_ff 512 \
  --top_k 5 \
  --des 'Exp' \
  --batch_size 16 \
  --itr 1

model_name=TimesNet
python -u run.py \
  --task_name long_term_forecast \
  --is_training 0 \
  --root_path /home/lenovo/yinzhou/dataset \
  --data_path 20250101_20250327.csv \
  --test_data_path 20250328_20250328.csv \
  --model_id custom_timesnet \
  --model $model_name \
  --data custom \
  --freq s \
  --patience 7 \
  --train_epochs 20 \
  --features MS \
  --target 93 \
  --seq_len 256 \
  --label_len 128 \
  --pred_len 1 \
  --e_layers 2 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 92 \
  --dec_in 92 \
  --c_out 1 \
  --des 'Exp' \
  --d_model 32 \
  --d_ff 32 \
  --top_k 5 \
  --itr 1 \
  --inverse