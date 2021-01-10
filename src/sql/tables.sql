drop table if exists fms_key_config;
create table fms_key_config
(
  id        int not null AUTO_INCREMENT,
  city      varchar(4),
  appKey    varchar(32),
  appSecret varchar(32),
  token     varchar(36),
  operator  varchar(30),
  tokenName varchar(30),
  status    int,
  orgCode   int,
  orgName   varchar(100),
  platCode  varchar(10),
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='三方token';

drop table if exists fms_third_shopinfo;
create table fms_third_shopinfo
(
  id          int not null AUTO_INCREMENT,
  thirdShopId varchar(24),
  name        varchar(200),
  shopId      int,
  platformId  int,
  thirdName   varchar(200),
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='三方店铺';

drop table if exists fms_wm_bill;
create table fms_wm_bill
(
  id                        varchar(50) not null,
  bill_charge_type          int comment '结算类型',
  charge_fee_desc           varchar(64) comment '结算类型描述',
  user_pay_type             varchar(64) comment '用户支付方式 -1-未知；1-货到付款；2-在线支付。目前外卖订单仅支持在线支付',
  wm_poi_order_push_day_seq varchar(64) comment '订单流水号',
  wm_order_view_id          varchar(64) comment '订单展示ID',
  order_time                datetime default null comment '订单下单时间',
  finish_time               datetime default null comment '订单完成时间',
  refund_time               datetime default null comment '订单退款时间',
  order_state               int comment '订单当前状态',
  shipping_type             int comment '订单配送方式',
  shipping_status           int comment '配送状态',
  account_state             int comment '结算状态',
  daliy_bill_date           int comment '账单日期',
  settle_bill_desc          varchar(64) comment '归账日期',
  settle_amount             DECIMAL comment '商家应收款',
  total_food_amount         DECIMAL comment '商品总价（不含商品包装盒费）',
  box_amount                DECIMAL comment '商品包装盒费总价',
  activity_poi_amount       DECIMAL comment '商家活动总支出金额（含赠品成本）',
  activity_meituan_amount   DECIMAL comment '美团活动补贴总金额',
  activity_agent_amount     DECIMAL comment '代理商活动承担金额',
  platform_charge_fee       DECIMAL comment '平台服务费',
  performance_service_fee   DECIMAL comment '订单履约服务费金额',
  user_pay_shipping_amount  DECIMAL comment '用户支付配送费',
  user_online_pay_amount    DECIMAL comment '用户在线支付金额',
  user_offline_pay_amount   DECIMAL comment '用户线下支付金额',
  rate                      DECIMAL comment '平台服务费的费率',
  bottom                    varchar(64) comment '保底金额',
  refund_id                 bigint comment '退款id',
  discount                  DECIMAL comment '分成折扣',
  settle_milli              DECIMAL comment '结算金额',
  settle_setting_id         varchar(64) comment '结算id',
  wm_donation_amount        DECIMAL comment '青山计划-公益捐赠金额',
  wm_doggy_bag_amount       DECIMAL comment '商超-打包袋金额',
  deal_tip                  DECIMAL comment '配送小费',
  product_preferences       bigint comment '商家活动支出分摊到商品上的优惠总金额',
  not_product_preferences   bigint comment '商家活动支出的未分摊到商品上的总金额',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='财务系统美团账单';

drop table if exists fms_channel_info;
create table fms_channel_info
(
  id            int not null AUTO_INCREMENT,
  channelCode   varchar(10) comment '渠道编码',
  channelName   varchar(100) comment '渠道名称',
  settleCircle  int comment '账单周期',
  settleGetTime varchar(50) comment '账单获取时间',
  creator       varchar(50),
  createDate    int comment '创建时间',
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='渠道信息管理';

drop table if exists fms_task_info;
create table fms_task_info
(
  id            int not null AUTO_INCREMENT,
  channelCode   varchar(10) comment '渠道编号',
  settleTime    int comment '账单日期',
  excelTotal    int comment 'excel数量',
  apiTotal      int comment '接口数量',
  opTotal       int comment '处理数量',
  apiState      varchar(30) comment '操作状态，waiting,loading,success',
  opState       varchar(30) comment '操作状态，reading,formatting,checking,over',
  rtState       varchar(30) comment '结果状态，running,fail,success',
  creator       varchar(50) comment '创建人',
  createDate    int comment '创建时间',
  startRead     int comment 'Read开始时间',
  endRead       int comment 'Read结束时间',
  startFormat   int comment 'Format开始时间',
  endFormat     int comment 'Format结束时间',
  startCheck    int comment 'Check开始时间',
  endCheck      int comment 'Check结束时间',
  startLoad     int comment 'LoadApi开始时间',
  endLoad       int comment 'LoadApi结束时间',
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务处理列表';

drop table if exists fms_third_bill;
create table fms_third_bill
(
  id                   bigint(20) not null AUTO_INCREMENT,
  thirdOrderId         VARCHAR(200) not null,
  payType              int not null,
  amount               int not null,
  status               int not null default '1' comment '对账状态 1 未核对 2 已核对-自动 3 核对失败 4 已核对-人工',
  createdAt            datetime default null,
  createdBy            VARCHAR(20),
  type                 int comment '类型 （1、收款 2、退款）',
  checkAmount          int comment '核对金额',
  checkAt              datetime default null,
  checkBy              VARCHAR(20),
  serviceCharge        int comment '服务费',
  payAt                datetime default null comment '支付时间',
  settleStatus         int default 1 not null comment '结算状态',
  channelDiscountPay   int comment '渠道优惠金额',
  orderPayAt           datetime default null comment '下单时间',
  receivePayTime       datetime default null comment '到账时间',
  businessTime         datetime default null comment '业务时间',
  diffAmount           int comment '账单差异',
  deliverPay           int comment '运费',
  accountDate          datetime default null comment '账单日期',
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='三方账单';

alter table fms_third_bill add index idx_type_thdOrdId(type, thirdOrderId);

drop table if exists fms_excel_path;
create table fms_excel_path
(
  id          int not null AUTO_INCREMENT,
  name        varchar(200),
  path        varchar(300),
  createDate    int comment '创建时间',
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Excel文件路径';