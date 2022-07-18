/* DROP */
DROP TABLE IF EXISTS `dbvidevino`.`tb_loja`;
drop table `dbvidevino`.`tb_pedido`;
drop table `dbvidevino`.`tb_vendas`;

/* CREATE */
CREATE TABLE IF NOT EXISTS `dbvidevino`.`tb_loja` (
  `id_loja` INT NOT NULL AUTO_INCREMENT,
  `desc_loja` VARCHAR(100) NULL,
  `desc_loja_apelido` VARCHAR(50) NULL,
  `dt_insert` DATE NULL,
  `dt_update` DATE NULL,
  PRIMARY KEY (`id_loja`))
PACK_KEYS = DEFAULT;
;
CREATE TABLE IF NOT EXISTS `dbvidevino`.`tb_origem` (
  `id_origem` INT NOT NULL AUTO_INCREMENT,
  `desc_origem` VARCHAR(100) NULL,
  `dt_insert` DATE NULL,
  `dt_update` DATE NULL,
  PRIMARY KEY (`id_origem`))
PACK_KEYS = DEFAULT;
;
CREATE TABLE IF NOT EXISTS `dbvidevino`.`tb_cliente` (
  `id_cliente` BIGINT NOT NULL,
  `codigo` INT NOT NULL,
  `nome` VARCHAR(100) NULL,
  `tipo_pessoa` VARCHAR(2) NULL,
  `cpf_cnpj` VARCHAR(18) NULL,
  `endereco` VARCHAR(100) NULL,
  `numero` VARCHAR(10) NULL,
  `complemento` VARCHAR(50) NULL,
  `bairro` VARCHAR(50) NULL,
  `cep` VARCHAR(10) NULL,
  `cidade` VARCHAR(50) NULL,
  `uf` VARCHAR(30) NULL,
  `situacao` VARCHAR(20) NULL,
  `data_criacao` DATETIME,
  `dt_insert` DATE NULL,
  `dt_update` DATE NULL,
  PRIMARY KEY (`id_cliente`))
PACK_KEYS = DEFAULT;
;
CREATE TABLE IF NOT EXISTS `dbvidevino`.`tb_produto` (
  `id_produto` BIGINT NOT NULL,
  `codigo` INT NOT NULL,
  `nome` VARCHAR(150) NULL,
  `preco` DECIMAL NULL,
  `preco_promocional` DECIMAL NULL,
  `unidade` VARCHAR(10) NULL,
  `gtin` VARCHAR(20) NULL,
  `tipo_variacao` VARCHAR(2) NULL,
  `localizacao` VARCHAR(100) NULL,
  `preco_custo` DECIMAL NULL,
  `preco_custo_medio` DECIMAL NULL,
  `situacao` VARCHAR(30) NULL,
  `dt_insert` DATE NULL,
  `dt_update` DATE NULL,
  PRIMARY KEY (`id_produto`))
PACK_KEYS = DEFAULT;
;
CREATE TABLE IF NOT EXISTS `dbvidevino`.`tb_pedido` (
  `id_seq_pedido` INT NOT NULL AUTO_INCREMENT,
  `id_seq_loja` INT NOT NULL,
  `id_pedido` BIGINT NOT NULL,
  `data_pedido` DATE NULL,
  `dt_insert` DATE NULL,
  PRIMARY KEY (`id_seq_pedido`))
PACK_KEYS = DEFAULT;
;
CREATE TABLE IF NOT EXISTS `dbvidevino`.`tb_vendas` (
  `id_seq_venda` INT NOT NULL AUTO_INCREMENT,
  `id_seq_loja` INT NOT NULL,
  `id_pedido` BIGINT NOT NULL,
  `data_pedido` DATE NULL,
  `cliente_nome` VARCHAR(100) NULL,
  `cliente_cpf_cnpj` VARCHAR(20) NULL,
  `numero_ordem_compra` VARCHAR(20) NULL,
  `situacao` VARCHAR(20) NULL,
  `item_id_produto` BIGINT NULL,
  `item_codigo` VARCHAR(30) NULL,
  `item_descricao` VARCHAR(150) NULL,
  `item_quantidade` DECIMAL NULL,
  `item_valor_unitario` DECIMAL NULL,
  `valor_frete` DECIMAL NULL,
  `valor_desconto` DECIMAL NULL,
  `outras_despesas` DECIMAL NULL,
  `total_produtos` DECIMAL NULL,
  `total_pedido` DECIMAL NULL,
  `dt_insert` DATE NULL,
  PRIMARY KEY (`id_seq_venda`))
PACK_KEYS = DEFAULT;
;

/* INSERT */
INSERT INTO `dbvidevino`.`tb_loja` (id_loja, desc_loja, desc_loja_apelido, dt_insert, dt_update) VALUES(-1,'Não Informado','NI',sysdate(),null);
INSERT INTO `dbvidevino`.`tb_loja` (id_loja, desc_loja, desc_loja_apelido, dt_insert, dt_update) VALUES(-2,'Não se Aplica','NA',sysdate(),null);
INSERT INTO `dbvidevino`.`tb_loja` (desc_loja, desc_loja_apelido, dt_insert, dt_update) VALUES('Videvino Morumbi','Morumbi',sysdate(),null);
INSERT INTO `dbvidevino`.`tb_loja` (desc_loja, desc_loja_apelido, dt_insert, dt_update) VALUES('Videvino Santo Amaro','Santo Amaro',sysdate(),null);
INSERT INTO `dbvidevino`.`tb_loja` (desc_loja, desc_loja_apelido, dt_insert, dt_update) VALUES('Videvino Centro','Centro',sysdate(),null);

INSERT INTO `dbvidevino`.`tb_origem` (id_origem, desc_origem, dt_insert, dt_update) VALUES(-1,'Não Informado','NI',sysdate(),null);
INSERT INTO `dbvidevino`.`tb_origem` (id_origem, desc_origem, dt_insert, dt_update) VALUES(-2,'Não se Aplica','NA',sysdate(),null);
INSERT INTO `dbvidevino`.`tb_origem` (desc_origem, dt_insert, dt_update) VALUES('Tiny',sysdate(),null);
INSERT INTO `dbvidevino`.`tb_origem` (desc_origem, dt_insert, dt_update) VALUES('Ifood',sysdate(),null);

INSERT INTO `dbvidevino`.`tb_cliente` (id_cliente, codigo, nome, tipo_pessoa, cpf_cnpj, dt_insert, dt_update) VALUES(-1,-1,'Não Informado','NI','-1',sysdate(),null);
INSERT INTO `dbvidevino`.`tb_cliente` (id_cliente, codigo, nome, tipo_pessoa, cpf_cnpj, dt_insert, dt_update) VALUES(-2,-2,'Não se Aplica','NA','-2',sysdate(),null);

INSERT INTO `dbvidevino`.`tb_produto` (id_produto, codigo, nome, dt_insert, dt_update) VALUES(-1,-1,'Não Informado',sysdate(),null);
INSERT INTO `dbvidevino`.`tb_produto` (id_produto, codigo, nome, dt_insert, dt_update) VALUES(-2,-2,'Não se Aplica',sysdate(),null);

