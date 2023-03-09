package com.vam.model;

import java.util.List;

import lombok.Data;

@Data
public class ReplyPageDTO {

	List<ReplyDTO> list;

	PageDTO pageInfo;

}
