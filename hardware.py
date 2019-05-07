#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wmi

c = wmi.WMI()


# 处理器
def get_cpu_info():
    boards = []
    for cpu in c.Win32_Processor():
        tmpdict = {}
        tmpdict["CpuCores"] = 0
        # tmpdict["cpuid"] = cpu.ProcessorId.strip()
        tmpdict["CpuType"] = cpu.Name
        # tmpdict['systemName'] = cpu.SystemName
        try:
            tmpdict["CpuCores"] = cpu.NumberOfCores
        except:
            tmpdict["CpuCores"] += 1
        # tmpdict["CpuClock"] = cpu.MaxClockSpeed
        # tmpdict['DataWidth'] = cpu.DataWidth
        boards.append(tmpdict)
    return boards


# 主板
def get_mainboard_info():
    boards = []
    for board_id in c.Win32_BaseBoard():
        tmpmsg = {}
        # tmpmsg['UUID'] = board_id.qualifiers['UUID'][1:-1]  # 主板UUID,有的主板这部分信息取到为空值，ffffff-ffffff这样的
        # tmpmsg['SerialNumber'] = board_id.SerialNumber  # 主板序列号
        # tmpmsg['Manufacturer'] = board_id.Manufacturer  # 主板生产品牌厂家
        # tmpmsg['Product'] = board_id.Product  # 主板型号
        boards.append(tmpmsg)
    return boards


# BIOS
def get_bios_info():
    bioss = []
    for bios_id in c.Win32_BIOS():
        tmpmsg = {}
        # tmpmsg['BiosCharacteristics'] = bios_id.BiosCharacteristics  # BIOS特征码
        # tmpmsg['version'] = bios_id.Version  # BIOS版本
        # tmpmsg['Manufacturer'] = bios_id.Manufacturer.strip()  # BIOS固件生产厂家
        # tmpmsg['ReleaseDate'] = bios_id.ReleaseDate  # BIOS释放日期
        # tmpmsg['SMBIOSBIOSVersion'] = bios_id.SMBIOSBIOSVersion  # 系统管理规范版本
        bioss.append(tmpmsg)
    return bioss


# 硬盘
def get_disk_info():
    disks = []
    for disk in c.Win32_DiskDrive():
        # print(disk)
        tmpmsg = {}
        # tmpmsg['UUID'] = disk.qualifiers['UUID'][1:-1]
        # tmpmsg['SerialNumber'] = disk.SerialNumber.strip()
        # tmpmsg['DeviceID'] = disk.DeviceID
        tmpmsg['Caption'] = disk.Caption
        tmpmsg['Size'] = disk.Size
        disks.append(tmpmsg)

    return disks


# 内存
def get_memory_info():
    memorys = []
    for mem in c.Win32_PhysicalMemory():
        # print(mem)
        tmpmsg = {}
        # tmpmsg['UUID'] = mem.qualifiers['UUID'][1:-1]
        # tmpmsg['BankLabel'] = mem.BankLabel
        # tmpmsg['SerialNumber'] = mem.SerialNumber.strip()
        tmpmsg['Capacity'] = mem.Capacity
        tmpmsg['Speed'] = mem.Speed
        # tmpmsg['ConfiguredVoltage'] = mem.ConfiguredVoltage
        tmpmsg['Manufacturer'] = str(mem.Manufacturer)
        memorys.append(tmpmsg)

    return memorys


# 网卡mac地址：
def get_network_info():
    networks = []
    for net in c.Win32_NetworkAdapter():
        tmpmsg = {}
        # PhysicalAdapter -- 指明适配器是否是物理或逻辑适配器。如果为True，适配器是物理
        if net.PhysicalAdapter:
            tmpmsg['Name'] = net.name
            tmpmsg['Manufacturer'] = net.Manufacturer
            networks.append(tmpmsg)
    return networks


def format_cpu_info(cpu_info):
    my_cpu = ''
    if len(cpu_info) == 0:
        my_cpu = '没有获取到CPU信息.\n'
    elif len(cpu_info) == 1:
        my_cpu = str(cpu_info[0].get('CpuCores')) + '核 ' + cpu_info[0].get('CpuType') + '\n'
    else:
        for i, val in enumerate(cpu_info):
            my_cpu += str(i + 1) + ':' + str(val.get('CpuCores')) + '核 ' + val.get('CpuType') + '\n'
    return my_cpu


def format_disk_info(disk_info):
    my_disk = ''
    if len(disk_info) == 0:
        my_disk = '没有获取到硬盘信息.\n'
    elif len(disk_info) == 1:
        disk_size = int(int(disk_info[0].get('Size')) / 1000 / 1000 / 1000)
        my_disk = str(disk_size) + 'GB ' + disk_info[0].get('Caption') + '\n'
    else:
        for i, val in enumerate(disk_info):
            disk_size = int(int(val.get('Size')) / 1000 / 1000 / 1000)
            my_disk += str(i + 1) + ':' + str(disk_size) + 'GB ' + val.get('Caption') + '\n'
    return my_disk


def format_memory_info(memory_info):
    my_memory = ''
    if len(memory_info) == 0:
        my_memory = '没有获取到内存信息.\n'
    elif len(memory_info) == 1:
        memory_size = int(int(memory_info[0].get('Capacity')) / 1024 / 1024 / 1024)
        my_memory = str(memory_size) + 'GB ' + str(memory_info[0].get('Speed')) + 'MHz Manufacturer:' + memory_info[
            0].get('Manufacturer') + '\n'
    else:
        for i, val in enumerate(memory_info):
            memory_size = int(int(val.get('Capacity')) / 1024 / 1024 / 1024)
            my_memory += str(i + 1) + ':' + str(memory_size) + 'GB ' + str(
                val.get('Speed')) + 'MHz Manufacturer:' + val.get('Manufacturer') + '\n'
    return my_memory


def format_network_info(network_info):
    my_network = ''
    if len(network_info) == 0:
        my_network = '没有获取到网卡信息.\n'
    elif len(network_info) == 1:
        my_network = str(network_info[0].get('Name')) + ' Manufacturer:' + network_info[0].get('Manufacturer') + '\n'
    else:
        for i, val in enumerate(network_info):
            my_network += str(i + 1) + ':' + str(val.get('Name')) + ' Manufacturer:' + val.get('Manufacturer') + '\n'
    return my_network


def get_hardware():
    cpu_info = get_cpu_info()
    disk_info = get_disk_info()
    memory_info = get_memory_info()
    network_info = get_network_info()

    print(format_cpu_info(cpu_info))
    print(format_disk_info(disk_info))
    print(format_memory_info(memory_info))
    print(format_network_info(network_info))

