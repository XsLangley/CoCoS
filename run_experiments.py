import os
import argparse


def main(args):
    model = args.model
    if model == 'Ogbn-arxiv':
        main_script = 'main_ogbnarxiv'
    else:
        main_script = 'main_small'

    num_round = args.round
    dataset =args.dataset
    pretr_states = args.pretr_state
    n_epochs = args.n_epochs
    n_step_epochs = args.n_step_epochs
    n_cls_pershuf = args.n_cls_pershuf
    n_layers = args.n_layers
    cls_layers = args.cls_layers
    dis_layers = args.dis_layers
    hid_dim = args.hid_dim
    emb_hid_dim = args.emb_hid_dim
    dropout = args.dropout
    idp = args.input_drop
    adp = args.attn_drop
    edp = args.attn_drop
    nh = args.num_heads
    agg_type = args.agg_type
    gpu = args.gpu
    lr = args.lr
    wd = args.weight_decay
    split = args.split
    wctr = args.wctr
    cls_mode = args.cls_mode
    ctr_mode = args.ctr_mode

    for r in range(num_round):
        run_cmd = "python -u {script}.py --model {m} --seed {seed} --dataset {db} --pretr_state {ptrst} " \
                  "--n_epochs {ep} --n_step_epochs {nsep} --n_cls_pershuf {ncps} " \
                  "--n_layers {nl} --cls_layers {cl} --dis_layers {dl} " \
                  "--hid_dim {hid_dim} --emb_hid_dim {ehd} " \
                  "--dropout {dp} --input_drop {idp} --attn_drop {adp} --edge_drop {edp} " \
                  "--num_heads {nh} --agg_type {at} " \
                  "--gpu {gpu} --lr {lr} --weight_decay {wd} --split {spt} " \
                  "--wctr {wctr} --cls_mode {clsm} --ctr_mode {ctrm} ".format(
            script=main_script, m=model, seed=r, db=dataset, ptrst=pretr_states,
            ep=n_epochs, nsep=n_step_epochs, ncps=n_cls_pershuf,
            nl=n_layers, cl=cls_layers, dl=dis_layers,
            hid_dim=hid_dim, ehd=emb_hid_dim,
            dp=dropout, idp=idp, adp=adp, edp=edp,
            nh=nh,  at=agg_type,
            gpu=gpu, lr=lr, wd=wd, spt=split,
            wctr=wctr, clsm=cls_mode, ctrm=ctr_mode,
            )
        os.system(run_cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reproduce the reported results of the paper. Repeatedly run a model.')
    parser.add_argument("--model", type=str, default='GCN',
                        help="model name")
    parser.add_argument("--round", type=int, default=10, help='number of rounds to repeat')
    parser.add_argument("--dataset", type=str, default='cora',
                        help="the dataset for the experiment")
    parser.add_argument("--pretr_state", type=str, default='val',
                        help="the version of the pretraining model")
    parser.add_argument("--n_epochs", type=int, default=1000,
                        help="the number of training epochs")
    parser.add_argument("--n_step_epochs", type=str, default='20',
                        help="the interval (epoch) to override/ update the estimated labels, corresponding to hyperparameter \eta")
    parser.add_argument("--n_cls_pershuf", type=int, default=4,
                        help="the number of classes for each shuffling operation, only works for Ogbn-arxiv")
    parser.add_argument("--n_layers", type=int, default=3,
                        help="the number of hidden layers")
    parser.add_argument("--cls_layers", type=int, default=1,
                        help="the number of MLP classifier layers, if any")
    parser.add_argument("--dis_layers", type=int, default=2,
                        help="the number of MLP discriminator layers, only for CoCoS-enhanced models")
    parser.add_argument("--hid_dim", type=str, default='256',
                        help="the hidden dimension of hidden layers in the backbone model")
    parser.add_argument("--emb_hid_dim", type=str, default='256',
                        help="the hidden dimension of the hidden layers in the MLP discriminator")
    parser.add_argument("--dropout", type=float, default=0.75,
                        help="dropout rate")
    parser.add_argument("--input_drop", type=float, default=0.25,
                        help="dropout for input features, only for models for Ogbn-arxiv")
    parser.add_argument("--attn_drop", type=float, default=0.0,
                        help="attention dropout rate, only for GAT for Ogbn-arxiv")
    parser.add_argument("--edge_drop", type=float, default=0.3,
                        help="edge dropout rate, only for GAT for Ogbn-arxiv")
    parser.add_argument("--num_heads", type=int, default=3,
                        help="the number of attention heads, only for GAT")
    parser.add_argument("--agg_type", type=str, default="gcn",
                        help="the aggregation type of GraphSAGE")
    parser.add_argument("--gpu", type=int, default=0,
                        help="specify the gpu index, set -1 to train on cpu")
    parser.add_argument("--lr", type=str, default='0.005',
                        help="the learning rate")
    parser.add_argument("--weight_decay", type=float, default=5e-4,
                        help="the weight decay for optimizer")
    parser.add_argument("--split", type=str, default='None',
                        help="the samples split settings, should be in the format of "
                             "{training set ratio}-{validation set ratio};"
                             "set None to use the standard train-val-test split of the dataset")
    parser.add_argument("--wctr", type=str, default='1',
                        help="coefficient for the contrastive loss, corresponding to alpha")
    parser.add_argument("--cls_mode", type=str, default='raw',
                        help="the type of the classification loss")
    parser.add_argument("--ctr_mode", type=str, default='F',
                        help="the type of positive pairs for contrastive loss")
    args = parser.parse_args()

    main(args)
