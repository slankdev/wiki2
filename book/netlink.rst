
Netlink Configuration Examples
==================================

base code
------------

rtnl

.. code-block:: c++

  #include "hexdump.h"
  #include "netlink.h"
  #include <stdio.h>
  #include <string.h>
  #include <stdlib.h>
  #include <arpa/inet.h>
  #include <netinet/in.h>

  void main() {
    int fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
    if (fd < 0)
      exit(1);

    ...(snip)...

    close(fd);
  }

genl

.. code-block:: c++

  #include "hexdump.h"
  #include "netlink.h"
  #include <stdio.h>
  #include <string.h>
  #include <stdlib.h>
  #include <arpa/inet.h>
  #include <netinet/in.h>

  void main() {
    int fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
    if (fd < 0)
      exit(1);

    ...(snip)...

    close(fd);
  }

get genl family id
-------------------

.. code-block:: c++

  static int get_family(int fd, const char *family_name)
  {
    GENL_REQUEST(req, 1024, GENL_ID_CTRL, 0,
        2, CTRL_CMD_GETFAMILY, NLM_F_REQUEST);
    addattrstrz(&req.n, 1024, CTRL_ATTR_FAMILY_NAME, family_name);

    char buf[10000];
    struct nlmsghdr *answer = (struct nlmsghdr*)buf;
    if (nl_talk(fd, &req.n, answer, sizeof(buf)) < 0)
      exit(1);

    int genl_family = -1;
    memcpy(&req, answer, sizeof(req));
    int len = req.n.nlmsg_len;
    if (NLMSG_OK(&req.n, len) ) {
      struct rtattr *rta[CTRL_ATTR_MAX + 1] = {};
      int l = req.n.nlmsg_len - NLMSG_LENGTH(sizeof(struct genlmsghdr));
      parse_rtattr(rta, CTRL_ATTR_MAX, (struct rtattr*)req.buf, l);

      if(rta[CTRL_ATTR_FAMILY_ID]) {
        uint16_t id = rta_getattr_u16(rta[CTRL_ATTR_FAMILY_ID]);
        genl_family = id;
      }
    }
          return genl_family;
  }

  void main() {
    int fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
    int genl_family = get_family(fd, "SEG6");
    printf("family_id: %d\n", genl_family);
    close(fd);
  }

sr tunsrc show
------------------

.. code-block:: c++

  static void show_sr_tunsrc(int fd, int genl_family)
  {
    GENL_REQUEST(req, 1024, genl_family, 0,
        SEG6_GENL_VERSION, SEG6_CMD_GET_TUNSRC, NLM_F_REQUEST);

    char buf[10000];
    struct nlmsghdr *answer = (struct nlmsghdr*)buf;
    if (nl_talk(fd, &req.n, answer, sizeof(buf)) < 0)
      exit(1);

    memcpy(&req, answer, sizeof(req));
    int len = req.n.nlmsg_len;
    if (NLMSG_OK(&req.n, len) ) {
      struct rtattr *rta[CTRL_ATTR_MAX + 1] = {};
      int l = req.n.nlmsg_len - NLMSG_LENGTH(sizeof(struct genlmsghdr));
      parse_rtattr(rta, CTRL_ATTR_MAX, (struct rtattr*)req.buf, l);

      if(rta[SEG6_ATTR_DST]) {
        const struct in6_addr *dst = RTA_DATA(rta[SEG6_ATTR_DST]);
        char str[128];
        inet_ntop(AF_INET6, dst, str, sizeof(str));
        printf("SRC: %s\n", str);
      }
    }
  }

  void main() {
    int fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
    int genl_family = get_family(fd, "SEG6");
    show_sr_tunsrc(fd, genl_family);
    close(fd);
  }

## sr tunsrc set

.. code-block:: c++

  static void set_sr_tunsrc(int fd, int genl_family, struct in6_addr *src)
  {
    GENL_REQUEST(req, 1024, genl_family, 0, SEG6_GENL_VERSION, SEG6_CMD_SET_TUNSRC, NLM_F_REQUEST);
    addattr_l(&req.n, sizeof(req), SEG6_ATTR_DST, src, sizeof(struct in6_addr));
    if (nl_talk(fd, &req.n, NULL, 0) < 0)
      exit(1);
  }

  void main() {
    int fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_GENERIC);
    int genl_family = get_family(fd, "SEG6");
    inet_pton(AF_INET6, "dd::", &src);
    set_sr_tunsrc(fd, genl_family, &src);
    close(fd);
  }

ip route add encap seg6
------------------------

.. code-block:: c++

  #include <stdio.h>
  #include <string.h>
  #include <stdlib.h>
  #include <arpa/inet.h>
  #include <netinet/in.h>
  #include <linux/seg6_iptunnel.h>
  #include <linux/lwtunnel.h>
  static void srh_dump(FILE* fp, struct ipv6_sr_hdr *srh)
  {
    fprintf(fp, "SRH\n");
    fprintf(fp, "+ nexthdr      : 0x%02x(%u)\n", srh->nexthdr      , srh->nexthdr      );
    fprintf(fp, "+ hdrlen       : 0x%02x(%u)\n", srh->hdrlen       , srh->hdrlen       );
    fprintf(fp, "+ type         : 0x%02x(%u)\n", srh->type         , srh->type         );
    fprintf(fp, "+ segments_left: 0x%02x(%u)\n", srh->segments_left, srh->segments_left);
    fprintf(fp, "+ first_segment: 0x%02x(%u)\n", srh->first_segment, srh->first_segment);
    fprintf(fp, "+ flags        : 0x%02x(%u)\n", srh->flags        , srh->flags        );
    fprintf(fp, "+ tag          : 0x%04x(%u)\n", srh->tag          , srh->tag          );
    fprintf(fp, "+ segments: [");
    const size_t n_loop = srh->segments_left + 1;
    for (size_t i=0; i<n_loop; i++) {
      char strbuf[100];
      inet_ntop(AF_INET6,
          (const void*)&srh->segments[i],
          strbuf, sizeof(strbuf));
      printf("%s%s", strbuf, i+1<n_loop?",":"]\n");
    }
  }

.. code-block:: c++

  static struct ipv6_sr_hdr *parse_srh(bool encap,
      size_t num_segs, struct in6_addr *segs)
  {
    const size_t srhlen = 8 + sizeof(struct in6_addr)*(encap ? num_segs+1 : num_segs);

    struct ipv6_sr_hdr *srh = malloc(srhlen);
    memset(srh, 0, srhlen);
    srh->hdrlen = (srhlen >> 3) - 1;
    srh->type = 4;
    srh->segments_left = encap ? num_segs : num_segs - 1;
    srh->first_segment = encap ? num_segs : num_segs - 1;

    size_t srh_idx = encap ? 1 : 0;
    for (ssize_t i=num_segs-1; i>=0; i--)
      memcpy(&srh->segments[srh_idx + i], &segs[num_segs - 1 - i], sizeof(struct in6_addr));
    return srh;
  }

  static void add_seg6_route(int fd,
      struct in_addr *pref, size_t plen,
      int mode, size_t num_segs, struct in6_addr *segs,
      uint32_t oif_idx)
  {
    struct {
      struct nlmsghdr  n;
      struct rtmsg r;
      char buf[4096];
    } req = {
      .n.nlmsg_len = NLMSG_LENGTH(sizeof(struct rtmsg)),
      .n.nlmsg_flags = NLM_F_REQUEST | NLM_F_CREATE | NLM_F_EXCL | NLM_F_ACK,
      .n.nlmsg_type = RTM_NEWROUTE,
      .r.rtm_family = AF_INET,
      .r.rtm_dst_len = plen,
      .r.rtm_src_len = 0,
      .r.rtm_tos = 0,
      .r.rtm_table = RT_TABLE_MAIN,
      .r.rtm_protocol = 0x03,
      .r.rtm_scope = 0xfd,
      .r.rtm_type = RTN_UNICAST,
      .r.rtm_flags = 0,
    };

    /* set RTA_DST */
    addattr_l(&req.n, sizeof(req), RTA_DST, pref, sizeof(struct in_addr));
    req.r.rtm_dst_len = plen;

    /* set RTA_OIF */
    addattr32(&req.n, sizeof(req), RTA_OIF, oif_idx);

    /* set RTA_ENCAP */
    char buf[1024];
    struct rtattr *rta = (void *)buf;
    rta->rta_type = RTA_ENCAP;
    rta->rta_len = RTA_LENGTH(0);
    struct rtattr *nest = rta_nest(rta, sizeof(buf), RTA_ENCAP);
    struct ipv6_sr_hdr *srh = parse_srh(false, num_segs, segs);
    size_t srhlen = (srh->hdrlen + 1) << 3;
    struct seg6_iptunnel_encap *tuninfo = malloc(sizeof(*tuninfo) + srhlen);
    memset(tuninfo, 0, sizeof(*tuninfo) + srhlen);
    memcpy(tuninfo->srh, srh, srhlen);
    tuninfo->mode = SEG6_IPTUN_MODE_ENCAP;
    rta_addattr_l(rta, sizeof(buf), SEG6_IPTUNNEL_SRH,
        tuninfo, sizeof(*tuninfo) + srhlen);
    rta_nest_end(rta, nest);
    addraw_l(&req.n, 1024 , RTA_DATA(rta), RTA_PAYLOAD(rta));

    /* set RTA_ENCAP_TYPE */
    addattr16(&req.n, sizeof(req), RTA_ENCAP_TYPE, LWTUNNEL_ENCAP_SEG6);

    if (nl_talk(fd, &req.n, NULL, 0) < 0)
      exit(1);
  }

.. code-block:: text

  /* 1.1.1.1  encap seg6 mode encap segs 2 [ 1:: 2:: ] dev dum0 scope link */
  monitoring group(RTMGRP) is 0xffffffff ...
  RTM_NEWROUTE f=0x0600 s=1571141704 p=0000028760 :: fmly=2 dl=32 sl=0 tos=0 tab=254 pro=3 scope=253 type=1 f=0x0
    0x000f RTA_TABLE        :: 254
    0x0001 RTA_DST          :: 1.1.1.1
    0x0004 RTA_OIF          :: 42
    0x0016 RTA_ENCAP        :: nested-data
      0x0001 SEG6_IPTUNNEL_SRH    :: mode=1 (SEG6_IPTUN_MODE_ENCAP) nh=0 hl=4 t=4 sl=1 [2::,1::]
    0x0015 RTA_ENCAP_TYPE   :: 5 (LWTUNNEL_ENCAP_SEG6)

  sudo ./ip/ip route add 1.1.1.2 encap seg6 mode encap segs 1::,2:: dev dum0
  0000:    68 00 00 00 18 00 05 06  56 c6 a5 5d 00 00 00 00   h.......  V..]....
  0010:    02 20 00 00 fe 03 fd 01  00 00 00 00 08 00 01 00   . ......  ........
  0020:    01 01 01 02 34 00 16 80  30 00 01 00 01 00 00 00   ....4...  0.......
  0030:    00 04 04 01 01 00 00 00  00 02 00 00 00 00 00 00   ........  ........
  0040:    00 00 00 00 00 00 00 00  00 01 00 00 00 00 00 00   ........  ........
  0050:    00 00 00 00 00 00 00 00  06 00 15 00 05 00 00 00   ........  ........
  0060:    08 00 04 00 2a 00 00 00                           ....*...

  sudo ./build/a.out
  0000:    68 00 00 00 18 00 05 06  00 00 00 00 00 00 00 00   h.......  ........
  0010:    02 20 00 00 fe 00 ff 01  00 00 00 00 08 00 01 00   . ......  ........
  0020:    01 01 01 02 08 00 04 00  2a 00 00 00 34 00 16 80   ........  *...4...
  0030:    30 00 01 00 01 00 00 00  00 04 04 01 01 00 00 00   0.......  ........
  0040:    00 01 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0050:    00 02 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0060:    06 00 15 00 05 00 00 00                           ........

ip route add encap seg6local End
--------------------------------

.. code-block:: c++

  static void add_seg6local_end_route(int fd,
      struct in6_addr *pref, size_t plen,
      uint32_t oif_idx)
  {
    struct {
      struct nlmsghdr  n;
      struct rtmsg r;
      char buf[4096];
    } req = {
      .n.nlmsg_len = NLMSG_LENGTH(sizeof(struct rtmsg)),
      .n.nlmsg_flags = NLM_F_REQUEST | NLM_F_CREATE | NLM_F_EXCL | NLM_F_ACK,
      .n.nlmsg_type = RTM_NEWROUTE,
      .r.rtm_family = AF_INET6,
      .r.rtm_dst_len = plen,
      .r.rtm_src_len = 0,
      .r.rtm_tos = 0,
      .r.rtm_table = RT_TABLE_MAIN,
      .r.rtm_protocol = 0x03,
      .r.rtm_scope = 0xfd,
      .r.rtm_type = RTN_UNICAST,
      .r.rtm_flags = 0,
    };

    /* set RTA_DST */
    addattr_l(&req.n, sizeof(req), RTA_DST, pref, sizeof(struct in6_addr));
    req.r.rtm_dst_len = plen;

    /* set RTA_OIF */
    addattr32(&req.n, sizeof(req), RTA_OIF, oif_idx);

    /* set RTA_ENCAP */
    char buf[1024];
    struct rtattr *rta = (void *)buf;
    rta->rta_type = RTA_ENCAP;
    rta->rta_len = RTA_LENGTH(0);
    struct rtattr *nest = rta_nest(rta, sizeof(buf), RTA_ENCAP);
    rta_addattr32(rta, sizeof(buf), SEG6_LOCAL_ACTION, SEG6_LOCAL_ACTION_END);
    rta_nest_end(rta, nest);
    addraw_l(&req.n, 1024 , RTA_DATA(rta), RTA_PAYLOAD(rta));

    /* set RTA_ENCAP_TYPE */
    addattr16(&req.n, sizeof(req), RTA_ENCAP_TYPE, LWTUNNEL_ENCAP_SEG6_LOCAL);

    hexdump(stdout, &req.n, req.n.nlmsg_len);
    if (nl_talk(fd, &req.n, NULL, 0) < 0)
      exit(1);
  }

.. code-block:: text

  sudo nlsniff -g all
  monitoring group(RTMGRP) is 0xffffffff ...
  RTM_NEWROUTE f=0x0600 s=1571166864 p=0000006645 :: fmly=10 dl=128 sl=0 tos=0 tab=254 pro=3 scope=0 type=1 f=0x0
    0x000f RTA_TABLE        :: 254
    0x0001 RTA_DST          :: 1::
    0x0006 RTA_PRIORITY     :: 1024
    0x0004 RTA_OIF          :: 42
    0x0016 RTA_ENCAP        :: nested-data
      0x0001 SEG6_LOCAL_ACTION    :: 1 (SEG6_LOCAL_ACTION_END)
    0x0015 RTA_ENCAP_TYPE   :: 7 (LWTUNNEL_ENCAP_SEG6_LOCAL)
    0x000c RTA_CACHEINFO    :: unknown-fmt(rta_len=36,data=01000000...)
    0x0014 RTA_PREF         :: 0

  sudo ./ip/ip route add 1:: encap seg6local action End dev dum0
  0000:    4c 00 00 00 18 00 05 06  90 1a a6 5d 00 00 00 00   L.......  ...]....
  0010:    0a 80 00 00 fe 03 00 01  00 00 00 00 14 00 01 00   ........  ........
  0020:    00 01 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0030:    0c 00 16 80 08 00 01 00  01 00 00 00 06 00 15 00   ........  ........
  0040:    07 00 00 00 08 00 04 00  2a 00 00 00               ........  *...

  sudo ./build/a.out
  0000:    4c 00 00 00 18 00 05 06  00 00 00 00 00 00 00 00   L.......  ........
  0010:    0a 80 00 00 fe 03 fd 01  00 00 00 00 14 00 01 00   ........  ........
  0020:    00 f1 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0030:    08 00 04 00 2a 00 00 00  0c 00 16 80 08 00 01 00   ....*...  ........
  0040:    01 00 00 00 06 00 15 00  07 00 00 00               ........  ....

ip route add encap seg6local End.X
----------------------------------

.. code-block:: c++

  static void add_seg6local_end_x_route(int fd,
      struct in6_addr *pref, size_t plen,
      struct in6_addr *nh6,
      uint32_t oif_idx)
  {
    struct {
      struct nlmsghdr  n;
      struct rtmsg r;
      char buf[4096];
    } req = {
      .n.nlmsg_len = NLMSG_LENGTH(sizeof(struct rtmsg)),
      .n.nlmsg_flags = NLM_F_REQUEST | NLM_F_CREATE | NLM_F_EXCL | NLM_F_ACK,
      .n.nlmsg_type = RTM_NEWROUTE,
      .r.rtm_family = AF_INET6,
      .r.rtm_dst_len = plen,
      .r.rtm_src_len = 0,
      .r.rtm_tos = 0,
      .r.rtm_table = RT_TABLE_MAIN,
      .r.rtm_protocol = 0x03,
      .r.rtm_scope = 0xfd,
      .r.rtm_type = RTN_UNICAST,
      .r.rtm_flags = 0,
    };

    /* set RTA_DST */
    addattr_l(&req.n, sizeof(req), RTA_DST, pref, sizeof(struct in6_addr));
    req.r.rtm_dst_len = plen;

    /* set RTA_OIF */
    addattr32(&req.n, sizeof(req), RTA_OIF, oif_idx);

    /* set RTA_ENCAP */
    char buf[1024];
    struct rtattr *rta = (void *)buf;
    rta->rta_type = RTA_ENCAP;
    rta->rta_len = RTA_LENGTH(0);
    struct rtattr *nest = rta_nest(rta, sizeof(buf), RTA_ENCAP);
    rta_addattr32(rta, sizeof(buf), SEG6_LOCAL_ACTION, SEG6_LOCAL_ACTION_END_X);
    rta_addattr_l(rta, sizeof(buf), SEG6_LOCAL_NH6, nh6, sizeof(struct in6_addr));
    rta_nest_end(rta, nest);
    addraw_l(&req.n, 1024 , RTA_DATA(rta), RTA_PAYLOAD(rta));

    /* set RTA_ENCAP_TYPE */
    addattr16(&req.n, sizeof(req), RTA_ENCAP_TYPE, LWTUNNEL_ENCAP_SEG6_LOCAL);

    hexdump(stdout, &req.n, req.n.nlmsg_len);
    if (nl_talk(fd, &req.n, NULL, 0) < 0)
      exit(1);
  }

.. code-block:: text

  sudo nlsniff -g all
  monitoring group(RTMGRP) is 0xffffffff ...
  RTM_NEWROUTE f=0x0600 s=1571167833 p=0000021250 :: fmly=10 dl=128 sl=0 tos=0 tab=254 pro=3 scope=0 type=1 f=0x0
    0x000f RTA_TABLE        :: 254
    0x0001 RTA_DST          :: f1::
    0x0006 RTA_PRIORITY     :: 1024
    0x0004 RTA_OIF          :: 42
    0x0016 RTA_ENCAP        :: nested-data
      0x0001 SEG6_LOCAL_ACTION    :: 2 (SEG6_LOCAL_ACTION_END_X)
      0x0005 SEG6_LOCAL_NH6       :: 2001::2
    0x0015 RTA_ENCAP_TYPE   :: 7 (LWTUNNEL_ENCAP_SEG6_LOCAL)
    0x000c RTA_CACHEINFO    :: unknown-fmt(rta_len=36,data=01000000...)
    0x0014 RTA_PREF         :: 0

  sudo ./ip/ip route add f1:: encap seg6local action End.X nh6 2001::2 dev dum0
  0000:    60 00 00 00 18 00 05 06  59 1e a6 5d 00 00 00 00   `.......  Y..]....
  0010:    0a 80 00 00 fe 03 00 01  00 00 00 00 14 00 01 00   ........  ........
  0020:    00 f1 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0030:    20 00 16 80 08 00 01 00  02 00 00 00 14 00 05 00    .......  ........
  0040:    20 01 00 00 00 00 00 00  00 00 00 00 00 00 00 02    .......  ........
  0050:    06 00 15 00 07 00 00 00  08 00 04 00 2a 00 00 00   ........  ....*...

  sudo ./build/a.out
  0000:    60 00 00 00 18 00 05 06  00 00 00 00 00 00 00 00   `.......  ........
  0010:    0a 80 00 00 fe 03 fd 01  00 00 00 00 14 00 01 00   ........  ........
  0020:    00 f1 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0030:    08 00 04 00 2a 00 00 00  20 00 16 80 08 00 01 00   ....*...   .......
  0040:    02 00 00 00 14 00 05 00  20 01 00 00 00 00 00 00   ........   .......
  0050:    00 00 00 00 00 00 00 02  06 00 15 00 07 00 00 00   ........  ........

ip route add encap seg6local End.T
-----------------------------------

.. code-block:: c++

  static void add_seg6local_end_t_route(int fd,
      struct in6_addr *pref, size_t plen,
                  uint32_t table_id,
      uint32_t oif_idx)
  {
    struct {
      struct nlmsghdr  n;
      struct rtmsg r;
      char buf[4096];
    } req = {
      .n.nlmsg_len = NLMSG_LENGTH(sizeof(struct rtmsg)),
      .n.nlmsg_flags = NLM_F_REQUEST | NLM_F_CREATE | NLM_F_EXCL | NLM_F_ACK,
      .n.nlmsg_type = RTM_NEWROUTE,
      .r.rtm_family = AF_INET6,
      .r.rtm_dst_len = plen,
      .r.rtm_src_len = 0,
      .r.rtm_tos = 0,
      .r.rtm_table = RT_TABLE_MAIN,
      .r.rtm_protocol = 0x03,
      .r.rtm_scope = 0xfd,
      .r.rtm_type = RTN_UNICAST,
      .r.rtm_flags = 0,
    };

    /* set RTA_DST */
    addattr_l(&req.n, sizeof(req), RTA_DST, pref, sizeof(struct in6_addr));
    req.r.rtm_dst_len = plen;

    /* set RTA_OIF */
    addattr32(&req.n, sizeof(req), RTA_OIF, oif_idx);

    /* set RTA_ENCAP */
    char buf[1024];
    struct rtattr *rta = (void *)buf;
    rta->rta_type = RTA_ENCAP;
    rta->rta_len = RTA_LENGTH(0);
    struct rtattr *nest = rta_nest(rta, sizeof(buf), RTA_ENCAP);
          rta_addattr32(rta, sizeof(buf), SEG6_LOCAL_ACTION, SEG6_LOCAL_ACTION_END_T);
          rta_addattr32(rta, sizeof(buf), SEG6_LOCAL_TABLE, table_id);
    rta_nest_end(rta, nest);
    addraw_l(&req.n, 1024 , RTA_DATA(rta), RTA_PAYLOAD(rta));

    /* set RTA_ENCAP_TYPE */
    addattr16(&req.n, sizeof(req), RTA_ENCAP_TYPE, LWTUNNEL_ENCAP_SEG6_LOCAL);

    hexdump(stdout, &req.n, req.n.nlmsg_len);
    if (nl_talk(fd, &req.n, NULL, 0) < 0)
      exit(1);
  }

.. code-block:: text

  sudo nlsniff -g all
  monitoring group(RTMGRP) is 0xffffffff ...
  RTM_NEWROUTE f=0x0600 s=1571168033 p=0000005254 :: fmly=10 dl=128 sl=0 tos=0 tab=254 pro=3 scope=0 type=1 f=0x0
    0x000f RTA_TABLE        :: 254
    0x0001 RTA_DST          :: f2::
    0x0006 RTA_PRIORITY     :: 1024
    0x0004 RTA_OIF          :: 42
    0x0016 RTA_ENCAP        :: nested-data
      0x0001 SEG6_LOCAL_ACTION    :: 3 (SEG6_LOCAL_ACTION_END_T)
      0x0003 SEG6_LOCAL_TABLE     :: 10
    0x0015 RTA_ENCAP_TYPE   :: 7 (LWTUNNEL_ENCAP_SEG6_LOCAL)
    0x000c RTA_CACHEINFO    :: unknown-fmt(rta_len=36,data=01000000...)
    0x0014 RTA_PREF         :: 0

  sudo ./ip/ip route add f2:: encap seg6local action End.T table 10 dev dum0
  0000:    54 00 00 00 18 00 05 06  21 1f a6 5d 00 00 00 00   T.......  !..]....
  0010:    0a 80 00 00 fe 03 00 01  00 00 00 00 14 00 01 00   ........  ........
  0020:    00 f2 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0030:    14 00 16 80 08 00 01 00  03 00 00 00 08 00 03 00   ........  ........
  0040:    0a 00 00 00 06 00 15 00  07 00 00 00 08 00 04 00   ........  ........
  0050:    2a 00 00 00                                       *...

  sudo ./build/a.out
  0000:    54 00 00 00 18 00 05 06  00 00 00 00 00 00 00 00   T.......  ........
  0010:    0a 80 00 00 fe 03 fd 01  00 00 00 00 14 00 01 00   ........  ........
  0020:    00 f1 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0030:    08 00 04 00 2a 00 00 00  14 00 16 80 08 00 01 00   ....*...  ........
  0040:    03 00 00 00 08 00 03 00  0a 00 00 00 06 00 15 00   ........  ........
  0050:    07 00 00 00                                       ....

ip route add encap seg6local End.DX4
------------------------------------

.. code-block:: c++

  static void add_seg6local_end_dx4_route(int fd,
      struct in6_addr *pref, size_t plen,
                  struct in_addr *nh4,
      uint32_t oif_idx)
  {
    struct {
      struct nlmsghdr  n;
      struct rtmsg r;
      char buf[4096];
    } req = {
      .n.nlmsg_len = NLMSG_LENGTH(sizeof(struct rtmsg)),
      .n.nlmsg_flags = NLM_F_REQUEST | NLM_F_CREATE | NLM_F_EXCL | NLM_F_ACK,
      .n.nlmsg_type = RTM_NEWROUTE,
      .r.rtm_family = AF_INET6,
      .r.rtm_dst_len = plen,
      .r.rtm_src_len = 0,
      .r.rtm_tos = 0,
      .r.rtm_table = RT_TABLE_MAIN,
      .r.rtm_protocol = 0x03,
      .r.rtm_scope = 0xfd,
      .r.rtm_type = RTN_UNICAST,
      .r.rtm_flags = 0,
    };

    /* set RTA_DST */
    addattr_l(&req.n, sizeof(req), RTA_DST, pref, sizeof(struct in6_addr));
    req.r.rtm_dst_len = plen;

    /* set RTA_OIF */
    addattr32(&req.n, sizeof(req), RTA_OIF, oif_idx);

    /* set RTA_ENCAP */
    char buf[1024];
    struct rtattr *rta = (void *)buf;
    rta->rta_type = RTA_ENCAP;
    rta->rta_len = RTA_LENGTH(0);
    struct rtattr *nest = rta_nest(rta, sizeof(buf), RTA_ENCAP);
          rta_addattr32(rta, sizeof(buf), SEG6_LOCAL_ACTION, SEG6_LOCAL_ACTION_END_DX4);
          rta_addattr_l(rta, sizeof(buf), SEG6_LOCAL_NH4, nh4, sizeof(struct in_addr));
    rta_nest_end(rta, nest);
    addraw_l(&req.n, 1024 , RTA_DATA(rta), RTA_PAYLOAD(rta));

    /* set RTA_ENCAP_TYPE */
    addattr16(&req.n, sizeof(req), RTA_ENCAP_TYPE, LWTUNNEL_ENCAP_SEG6_LOCAL);

    hexdump(stdout, &req.n, req.n.nlmsg_len);
    if (nl_talk(fd, &req.n, NULL, 0) < 0)
      exit(1);
  }

.. code-block:: text

  RTM_NEWROUTE f=0x0600 s=1571168127 p=0000012831 :: fmly=10 dl=128 sl=0 tos=0 tab=254 pro=3 scope=0 type=1 f=0x0
    0x000f RTA_TABLE        :: 254
    0x0001 RTA_DST          :: f2::
    0x0006 RTA_PRIORITY     :: 1024
    0x0004 RTA_OIF          :: 42
    0x0016 RTA_ENCAP        :: nested-data
      0x0001 SEG6_LOCAL_ACTION    :: 6 (SEG6_LOCAL_ACTION_END_DX4)
      0x0004 SEG6_LOCAL_NH4       :: 10.0.0.2
    0x0015 RTA_ENCAP_TYPE   :: 7 (LWTUNNEL_ENCAP_SEG6_LOCAL)
    0x000c RTA_CACHEINFO    :: unknown-fmt(rta_len=36,data=01000000...)
    0x0014 RTA_PREF         :: 0

  sudo ./ip/ip route add f2:: encap seg6local action End.DX4 nh4 10.0.0.2 dev dum0
  0000:    54 00 00 00 18 00 05 06  7f 1f a6 5d 00 00 00 00   T.......  ...]....
  0010:    0a 80 00 00 fe 03 00 01  00 00 00 00 14 00 01 00   ........  ........
  0020:    00 f2 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0030:    14 00 16 80 08 00 01 00  06 00 00 00 08 00 04 00   ........  ........
  0040:    0a 00 00 02 06 00 15 00  07 00 00 00 08 00 04 00   ........  ........
  0050:    2a 00 00 00                                       *...

  sudo ./build/a.out
  0000:    54 00 00 00 18 00 05 06  00 00 00 00 00 00 00 00   T.......  ........
  0010:    0a 80 00 00 fe 03 fd 01  00 00 00 00 14 00 01 00   ........  ........
  0020:    00 f1 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ........  ........
  0030:    08 00 04 00 2a 00 00 00  14 00 16 80 08 00 01 00   ....*...  ........
  0040:    06 00 00 00 08 00 04 00  0a 00 00 02 06 00 15 00   ........  ........
  0050:    07 00 00 00                                       ....

ip {-6|-4} route {add|del} via NH
----------------------------------

.. code-block:: c++

  #include "hexdump.h"
  #include "netlink.h"
  #include <stdio.h>
  #include <stdbool.h>
  #include <string.h>
  #include <stdlib.h>
  #include <unistd.h>
  #include <arpa/inet.h>
  #include <netinet/in.h>

  static void adddel_in6_route(int fd,
      struct in6_addr *pref, uint32_t plen,
                  struct in6_addr *nh6, bool install)
  {
    struct {
      struct nlmsghdr  n;
      struct rtmsg r;
      char buf[4096];
    } req = {
      .n.nlmsg_len = NLMSG_LENGTH(sizeof(struct rtmsg)),
      .n.nlmsg_flags = NLM_F_REQUEST | NLM_F_CREATE | NLM_F_EXCL | NLM_F_ACK,
      .n.nlmsg_type = install ? RTM_NEWROUTE : RTM_DELROUTE,
      .r.rtm_family = AF_INET6,
      .r.rtm_dst_len = plen,
      .r.rtm_src_len = 0,
      .r.rtm_tos = 0,
      .r.rtm_table = RT_TABLE_MAIN,
      .r.rtm_protocol = 0x03,
      .r.rtm_scope = 0xfd,
      .r.rtm_type = RTN_UNICAST,
      .r.rtm_flags = 0,
    };

    /* set RTA_DST */
    addattr_l(&req.n, sizeof(req), RTA_DST, pref, sizeof(struct in6_addr));
    req.r.rtm_dst_len = plen;

    /* set RTA_GATEWAY */
    addattr_l(&req.n, sizeof(req), RTA_GATEWAY, nh6, sizeof(struct in6_addr));

    /* talk with netlink-bus */
    hexdump(stdout, &req.n, req.n.nlmsg_len);
    if (nl_talk(fd, &req.n, NULL, 0) < 0)
      exit(1);
  }

  void main() {
    int fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
    if (fd < 0)
      exit(1);

    struct in6_addr pref, nh6;
    uint32_t plen = 128;
    uint32_t num_segs = 3;
    inet_pton(AF_INET6, "20::", &pref);
    inet_pton(AF_INET6, "2001::2", &nh6);

    adddel_in6_route(fd, &pref, plen, &nh6, true);
    close(fd);
  }


ip link
-------

ip nexthop
-----------

.. code-block:: c++

  #include "netlink.h"
  #include "hexdump.h"
  #include <stdio.h>
  #include <stdbool.h>
  #include <string.h>
  #include <stdlib.h>
  #include <unistd.h>
  #include <arpa/inet.h>
  #include <netinet/in.h>
  #include <linux/nexthop.h>
  #include <linux/lwtunnel.h>
  #include <linux/seg6.h>
  #include <linux/seg6_local.h>
  #include <linux/seg6_iptunnel.h>

  static void adddel_nexthop(int fd,
      uint32_t oif_idx, uint32_t nh_id,
      bool install)
  {
    struct {
      struct nlmsghdr  n;
      struct nhmsg nh;
      char buf[4096];
    } req = {
      .n.nlmsg_len = NLMSG_LENGTH(sizeof(struct nhmsg)),
      .n.nlmsg_flags = NLM_F_REQUEST | NLM_F_CREATE | NLM_F_EXCL | NLM_F_ACK,
      .n.nlmsg_type = install ? RTM_NEWNEXTHOP : RTM_DELNEXTHOP,
      .nh.nh_family = AF_INET6,
      .nh.nh_scope = 0x00,
      .nh.nh_protocol = 0x03,
      .nh.resvd = 0x00,
      .nh.nh_flags = 0,
    };

    addattr32(&req.n, sizeof(req), NHA_OIF, oif_idx);
    addattr32(&req.n, sizeof(req), NHA_ID, nh_id);
    addattr16(&req.n, sizeof(req), NHA_ENCAP_TYPE, LWTUNNEL_ENCAP_SEG6_LOCAL);

    char buf[1024];
    struct rtattr *rta = (void *)buf;
    rta->rta_type = NHA_ENCAP;
    rta->rta_len = RTA_LENGTH(0);
    struct rtattr *nest = rta_nest(rta, sizeof(buf), NHA_ENCAP);
    rta_addattr32(rta, sizeof(buf), SEG6_LOCAL_ACTION, SEG6_LOCAL_ACTION_END);
    rta_nest_end(rta, nest);
    addraw_l(&req.n, 1024 , RTA_DATA(rta), RTA_PAYLOAD(rta));

    int ret = nl_talk(fd, &req.n, NULL, 0):
    if (ret < 0)
      exit(1);
  }

  void main() {
    int fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
    if (fd < 0)
      exit(1);

    uint32_t oif_idx = 4;
    uint32_t nh_id = 22;
    adddel_nexthop(fd, oif_idx, nh_id, true);
    close(fd);
  }

